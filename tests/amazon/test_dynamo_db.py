import uuid
from unittest.mock import Mock, patch

import pytest
from botocore.exceptions import ClientError

from src.amazon.dynamo_db import DynamoDBClient
from src.exceptions import DDBException


@pytest.fixture
def mock_dynamodb_table():
    mock_table = Mock()
    mock_table.key_schema = [
        {"AttributeName": "itemId", "KeyType": "HASH"},
        {"AttributeName": "sortKey", "KeyType": "RANGE"}
    ]
    return mock_table


@pytest.fixture
def dynamodb_client(mock_dynamodb_table):
    mock_resource = Mock()
    mock_resource.Table.return_value = mock_dynamodb_table
    return DynamoDBClient(mock_resource, "test-table")


def test_init_client(dynamodb_client):
    assert dynamodb_client.hash_key_attribute_name == "itemId"
    assert dynamodb_client.range_key_attribute_name == "sortKey"


def test_get_all_table_items_empty(mock_dynamodb_table, dynamodb_client):
    mock_dynamodb_table.scan.return_value = {"Items": []}
    items = dynamodb_client.get_all_table_items()
    assert items == []
    mock_dynamodb_table.scan.assert_called_once()


def test_get_all_table_items_with_data(mock_dynamodb_table, dynamodb_client):
    test_items = [
        {"itemId": str(uuid.uuid4()), "sortKey": "test1", "data": "value1"},
        {"itemId": str(uuid.uuid4()), "sortKey": "test2", "data": "value2"},
    ]
    mock_dynamodb_table.scan.return_value = {"Items": test_items}

    items = dynamodb_client.get_all_table_items()
    assert len(items) == 2
    assert all(item["data"] in ["value1", "value2"] for item in items)
    mock_dynamodb_table.scan.assert_called_once()


def test_create_item_success(mock_dynamodb_table, dynamodb_client):
    item = {
        "itemId": str(uuid.uuid4()),
        "sortKey": "test",
        "data": "test_value"
    }
    mock_dynamodb_table.put_item.return_value = {}
    mock_dynamodb_table.get_item.return_value = {"Item": item}

    result = dynamodb_client.create_item(item)
    assert result == item
    mock_dynamodb_table.put_item.assert_called_once_with(Item=item)


def test_create_item_failure(mock_dynamodb_table, dynamodb_client):
    mock_dynamodb_table.put_item.side_effect = ClientError(
        operation_name="PutItem",
        error_response={
            "Error": {
                "Code": "ResourceNotFoundException",
                "Message": "Table not found",
            }
        }
    )

    with pytest.raises(DDBException):
        dynamodb_client.create_item({"itemId": "test", "sortKey": "test"})


def test_delete_item(mock_dynamodb_table, dynamodb_client):
    item_id = str(uuid.uuid4())
    sort_key = "test"
    mock_dynamodb_table.delete_item.return_value = {}

    dynamodb_client.delete_item(hash_key=item_id, sort_key=sort_key)

    mock_dynamodb_table.delete_item.assert_called_once_with(
        Key={
            'itemId': item_id,
            'sortKey': sort_key
        }
    )


def test_delete_all_items(mock_dynamodb_table, dynamodb_client):
    items = [
        {"itemId": str(uuid.uuid4()), "sortKey": "test1", "data": "value1"},
        {"itemId": str(uuid.uuid4()), "sortKey": "test2", "data": "value2"},
    ]
    mock_dynamodb_table.scan.return_value = {"Items": items}

    # Mock the batch writer context manager
    mock_batch_writer = Mock()
    mock_context_manager = Mock()
    mock_context_manager.__enter__ = Mock(return_value=mock_batch_writer)
    mock_context_manager.__exit__ = Mock()
    mock_dynamodb_table.batch_writer.return_value = mock_context_manager

    dynamodb_client.delete_all_items()

    mock_dynamodb_table.scan.assert_called_once()
    assert mock_batch_writer.delete_item.call_count == len(items)
    for item in items:
        mock_batch_writer.delete_item.assert_any_call(
            Key={
                "itemId": item["itemId"],
                "sortKey": item["sortKey"]
            }
        )


def test_get_item(mock_dynamodb_table, dynamodb_client):
    item_id = str(uuid.uuid4())
    item = {
        "itemId": item_id,
        "sortKey": "test",
        "data": "test_value"
    }
    mock_dynamodb_table.get_item.return_value = {"Item": item}

    result = dynamodb_client.get_item(item_id, "test")
    assert result == item
    mock_dynamodb_table.get_item.assert_called_once_with(
        Key={"itemId": item_id, "sortKey": "test"}
    )


def test_get_item_not_found(mock_dynamodb_table, dynamodb_client):
    mock_dynamodb_table.get_item.return_value = {}
    result = dynamodb_client.get_item(str(uuid.uuid4()), "test")
    assert result is None


def test_batch_write_items_success(mock_dynamodb_table, dynamodb_client):
    items = [
        {"itemId": str(uuid.uuid4()), "sortKey": "test1", "data": "value1"},
        {"itemId": str(uuid.uuid4()), "sortKey": "test2", "data": "value2"},
    ]

    # Mock the batch writer context manager
    mock_batch_writer = Mock()
    mock_context_manager = Mock()
    mock_context_manager.__enter__ = Mock(return_value=mock_batch_writer)
    mock_context_manager.__exit__ = Mock()
    mock_dynamodb_table.batch_writer.return_value = mock_context_manager

    dynamodb_client.batch_write_items(items)

    assert mock_batch_writer.put_item.call_count == len(items)
    for item in items:
        mock_batch_writer.put_item.assert_any_call(Item=item)


def test_batch_write_items_failure(mock_dynamodb_table, dynamodb_client):
    # Mock DynamoDB client that raises ClientError
    mock_dynamodb_table.batch_writer.side_effect = ClientError(
        operation_name="BatchWriteItem",
        error_response={
            "Error": {
                "Code": "ResourceNotFoundException",
                "Message": "Table not found",
            }
        }
    )

    with pytest.raises(DDBException):
        dynamodb_client.batch_write_items([{"itemId": "test", "sortKey": "test"}])
