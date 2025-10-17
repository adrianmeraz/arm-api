import boto3
from botocore.exceptions import ClientError
from pydantic.v1 import UUID4

from src import exceptions

_session = boto3.Session()
dynamodb = _session.resource('dynamodb')

class DynamoDBClient:
    def __init__(self, table_name: str):
        self._table = dynamodb.Table(table_name)

    def get_all_table_items(self, **kwargs):
        response = self._table.scan(**kwargs)
        return response.get('Items', [])

    def create_item(self, item: dict, **kwargs: dict):
        try:
            self._table.put_item(Item=item, **kwargs)
            return item
        except ClientError as e:
            raise exceptions.DDBException(detail=str(e))

    def get_item(self, item_id: UUID4, **kwargs: dict):
        response = self._table.get_item(Key={'itemId': item_id})
        return response.get('Item', None)
