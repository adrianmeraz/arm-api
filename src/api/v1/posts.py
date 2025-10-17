from typing import List

from fastapi import APIRouter

from src.models.post import Post
from src.amazon.dynamo_db import DynamoDBClient

router = APIRouter()


@router.get("/posts/", response_model=List[Post])
def read_posts():
    return DynamoDBClient("POSTS").get_all_table_items()
