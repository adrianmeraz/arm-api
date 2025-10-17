import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

class DynamoDBClient:
    def __init__(self, table_name):
        self._table = dynamodb.Table(table_name)

    def get_all_table_items(self):
        response = self._table.scan()
        return response.get('Items', [])
