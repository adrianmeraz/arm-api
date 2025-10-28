from typing import List

from fastapi import APIRouter

from src import logs
from src.data import post_data
from src.models.post import Post, PostOut

logger = logs.get_logger()
router = APIRouter()


@router.get("", response_model=List[PostOut])
def read_posts():
    return post_data.get_all_posts()

@router.post("", response_model=Post)
def create_post(post: Post):
    return post_data.create_post(post)

@router.delete("/{post_id}")
def delete_post(post_id: str):
    pk = Post.create_pk(obj_type='post', obj_id=post_id)
    logger.info(f'Deleting post with PK: {pk}, SK: {pk}')
    return post_data.delete_post(post_pk=pk)
