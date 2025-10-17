from typing import List

from fastapi import APIRouter

from src.amazon.dynamo_db import DynamoDBClient
from src.models.post import Post

router = APIRouter()
post_client = DynamoDBClient(table_name="POSTS")


@router.get("", response_model=List[Post])
def read_posts():
    posts = post_client.get_all_table_items()
    return posts

@router.post("", response_model=Post)
def create_post(post: Post):
    created_item = post_client.create_item(post.model_dump())
    return created_item
