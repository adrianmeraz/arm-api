from typing import List

from fastapi import APIRouter

from src import logs
from src.amazon import dynamodb, param_store
from src.amazon.dynamo_db import DynamoDBClient
from src.models.post import Post

logger = logs.get_logger()
router = APIRouter()
table_name = param_store.get_secret('AWS_DYNAMO_DB_TABLE_NAME')
post_client = DynamoDBClient(dynamodb_client=dynamodb, table_name=table_name)


@router.get("", response_model=List[Post])
def read_posts():
    posts = post_client.get_all_table_items()
    return posts

@router.post("", response_model=Post)
def create_post(post: Post):
    logger.info(f'Creating post.model_dump(): {post.model_dump(mode='json')}')
    created_item = post_client.create_item(post.model_dump(mode='json'))
    return created_item
