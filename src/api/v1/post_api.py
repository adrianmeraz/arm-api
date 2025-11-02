from typing import List, Optional

from fastapi import APIRouter

from src import decorators
from src import logs
from src.data import post_data
from src.models.post import Post, PostOut

logger = logs.get_logger()
router = APIRouter()


@router.get("/{post_id}", response_model=Optional[Post])
def get_post(post_id: str):
    return post_data.get_post(post_id)


@router.get("", response_model=List[PostOut])
def get_posts():
    return post_data.get_all_posts()

@router.post("", response_model=Post)
@decorators.require_dev_environment
def create_post(post: Post):
    return post_data.create_post(post)


@router.delete("/{post_id}")
@decorators.require_dev_environment
def delete_post(post_id: str):
    pk = sk = Post.generate_key(obj_type='post', obj_id=post_id)
    logger.info(f'Deleting post with PK: {pk}, SK: {sk}')
    return post_data.delete_post(post_pk=pk)

@router.delete("")
@decorators.require_dev_environment
def delete_all_posts():
    logger.info(f'Deleting all posts')
    return post_data.delete_all_posts()
