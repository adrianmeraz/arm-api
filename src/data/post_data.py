from src.amazon import dynamodb, param_store
from src.amazon.dynamo_db import DynamoDBClient
from src.models.post import Post

table_name = param_store.get_secret('AWS_DYNAMO_DB_TABLE_NAME')
post_client = DynamoDBClient(dynamodb_client=dynamodb, table_name=table_name)

def create_post(post: Post):
    return post_client.create_item(post.model_dump(mode='json'))

def batch_create_posts(posts: list[Post]):
    return post_client.batch_write_items([post.model_dump(mode='json') for post in posts])

def get_all_posts():
    return post_client.get_all_table_items()
