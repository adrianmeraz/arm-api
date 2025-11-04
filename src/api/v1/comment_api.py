from typing import List

from fastapi import APIRouter

from src import decorators
from src import logs
from src.data import comment_data
from src.models.comment import Comment

logger = logs.get_logger()
router = APIRouter()


@router.get("", response_model=List[Comment])
def get_comments(post_id: str):
    return comment_data.get_post_comments(post_id=post_id)


@router.get("/{comment_id}", response_model=Comment)
def get_comment(post_id: str, comment_id: str):
    """Get a single comment by its ID.

    Args:
        post_id: The ID of the post the comment belongs to
        comment_id: The ID of the comment to retrieve

    Returns:
        The comment if found
    """
    return comment_data.get_post_comment(post_id=post_id, comment_id=comment_id)


@router.post("", response_model=Comment)
@decorators.require_dev_environment
def create_comment(post_id: str, comment: Comment):
    comment.pk=post_id
    return comment_data.create_comment(comment=comment)


@router.delete("/{comment_id}")
@decorators.require_dev_environment
def delete_comment(post_id: str, comment_id: str):
    return comment_data.delete_post_comment(post_id=post_id, comment_id=comment_id)


@router.delete("")
@decorators.require_dev_environment
def delete_all_comments(post_id: str):
    logger.info(f'Deleting all comments')
    return comment_data.delete_all_post_comments(post_id=post_id)
