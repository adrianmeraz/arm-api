from typing import List

from fastapi import APIRouter

from src import logs
from src.data import comment_data
from src.models.comment import Comment

logger = logs.get_logger()
router = APIRouter()


@router.get("", response_model=List[Comment])
def read_comments():
    return comment_data.get_all_comments()


@router.post("", response_model=Comment)
def create_comment(comment: Comment):
    return comment_data.create_comment(comment)


@router.delete("/{comment_id}")
def delete_comment(comment_id: str):
    pk = Comment.generate_key(obj_type='COMMENT', obj_id=comment_id)
    # logger.info(f'Deleting comment with PK: {pk}, SK: {sk}')
    return comment_data.delete_comment(comment_pk=pk)


@router.delete("")
def delete_all_comments():
    logger.info(f'Deleting all comments')
    return comment_data.delete_all_comments()

