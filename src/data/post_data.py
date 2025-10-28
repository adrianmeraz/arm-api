from src.amazon import dynamodb, param_store
from src.amazon.dynamo_db import DynamoDBClient
from src.models.post import Post

_table_name = param_store.get_secret('AWS_DYNAMO_DB_TABLE_NAME')
_table_client = DynamoDBClient(dynamodb_client=dynamodb, table_name=_table_name)

def create_post(post: Post):
    return _table_client.create_item(post.model_dump(mode='json'))

def delete_post(post_pk: str):
    return _table_client._table.delete_item(Key={
        'pk': post_pk,
        'sk': post_pk,
    })

def batch_create_posts(posts: list[Post]):
    return _table_client.batch_write_items([post.model_dump(mode='json') for post in posts])

def get_all_posts():
    return _table_client.get_all_table_items()
