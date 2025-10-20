from typing import List

from fastapi import APIRouter

from src import logs
from src.amazon import dynamodb, param_store
from src.amazon.dynamo_db import DynamoDBClient
from src.models.post import Post

logger = logs.get_logger()
router = APIRouter()
# table_name = param_store.get_secret('AWS_DYNAMO_DB_TABLE_NAME')
table_name = 'arm-api-dev-table'
logger.info(f"Table name: {table_name}")
post_client = DynamoDBClient(dynamodb_client=dynamodb, table_name=table_name)


@router.get("", response_model=List[Post])
def read_posts():
    posts = post_client.get_all_table_items()
    return posts

@router.post("", response_model=Post)
def create_post(post: Post):
    created_item = post_client.create_item(post.model_dump())
    return created_item
