import typing

from boto3.resources.base import ServiceResource
from botocore.exceptions import ClientError
from pydantic.v1 import UUID4

from src import exceptions, logs

logger = logs.get_logger()


class DynamoDBClient:
    def __init__(self, dynamodb_client: ServiceResource, table_name: str):
        self._table = dynamodb_client.Table(table_name)
        self._key_schema = {schema['KeyType']: schema['AttributeName'] for schema in self._table.key_schema}

    @property
    def hash_key_attribute_name(self):
        return self._key_schema['HASH']

    @property
    def range_key_attribute_name(self):
        return self._key_schema['RANGE']

    def get_all_table_items(self, **kwargs):
        response = self._table.scan(**kwargs)
        return response.get('Items', [])

    def create_item(self, item: dict, **kwargs: dict):
        try:
            logger.info(f'Creating item: {item}')
            self._table.put_item(Item=item, **kwargs)
            return item
        except ClientError as e:
            raise exceptions.DDBException() from e

    def delete_item(self, hash_key: str, sort_key: str):
        return self._table.delete_item(
            Key={
                self.hash_key_attribute_name: hash_key,
                self.range_key_attribute_name: sort_key
            }
        )

    def delete_all_items(self):
        response = self._table.scan()
        data = response['Items']

        # Continue scanning if there are more items (pagination)
        while 'LastEvaluatedKey' in response:
            response = self._table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])

        # Batch delete items
        try:
            with self._table.batch_writer() as batch:
                for item in data:
                    batch.delete_item(Key={
                        self.hash_key_attribute_name: item[self.hash_key_attribute_name],
                        self.range_key_attribute_name: item[self.range_key_attribute_name]
                    })
        except ClientError as e:
            raise exceptions.DDBException() from e

    def get_item(self, item_id: UUID4, sort_key: str, **kwargs: dict):
        response = self._table.get_item(
            Key={
                self.hash_key_attribute_name: str(item_id),
                self.range_key_attribute_name: sort_key
            },
            **kwargs
        )
        return response.get('Item', None)

    def batch_write_items(self, items: typing.List[dict], **kwargs: dict):
        try:
            with self._table.batch_writer() as batch:
                logger.info(f'Writing {len(items)} batch items')
                for item in items:
                    try:
                        batch.put_item(Item=item, **kwargs)
                    except ClientError as e:
                        raise exceptions.DDBException() from e
        except ClientError as e:
            raise exceptions.DDBException() from e
