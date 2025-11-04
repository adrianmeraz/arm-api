from typing import List, Optional

from fastapi import APIRouter

from src import decorators
from src.data import post_data
from src.models.post import Post, PostOut

router = APIRouter()


@router.get("/{post_id}", response_model=Optional[Post])
def get_post(post_id: str):
    return post_data.get_post(post_id)


@router.get("", response_model=List[PostOut])
def get_posts(limit: int = 25):
    return post_data.get_all_posts(limit=limit)

@router.post("", response_model=Post)
@decorators.require_dev_environment
def create_post(post: Post):
    return post_data.create_post(post)


@router.delete("/{post_id}")
@decorators.require_dev_environment
def delete_post(post_id: str):
    return post_data.delete_post(post_id)

@router.delete("")
@decorators.require_dev_environment
def delete_all_posts():
    return post_data.delete_all_posts()
