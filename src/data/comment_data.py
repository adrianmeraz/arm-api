from src import logs
from src.amazon import dynamodb_client, dynamo_db, param_store
from src.amazon.dynamo_db import DynamoDBClient
from src.models.comment import Comment

_table_name = param_store.get_secret('AWS_DYNAMO_DB_TABLE_NAME')
_table_client = DynamoDBClient(dynamodb_client=dynamodb_client, table_name=_table_name)
logger = logs.get_logger()


def create_comment(comment: Comment):
    return _table_client.create_item(comment.model_dump(mode='json'))


def delete_post_comment(post_id: str, comment_id: str):
    """Delete a comment by its id.

    For simplicity this function treats the comment's partition and sort key
    as the same generated key `COMMENT#<comment_id>`. This mirrors the
    behavior used elsewhere in the codebase when only a single id is
    available (e.g. route parameter `comment_id`).

    Args:
        comment_id: The comment object id (not a full PK).

    Returns:
        The raw response from the DynamoDB client's delete_item.
        :param comment_id:
        :param post_id:
    """
    pk = dynamo_db.generate_key(obj_type='POST', obj_id=post_id)
    sk = dynamo_db.generate_key(obj_type='COMMENT', obj_id=comment_id)
    logger.info(f"Deleting comment with PK: {pk}, SK: {sk}")
    return _table_client.delete_item(hash_key=pk, sort_key=sk)


def get_post_comment(post_id: str, comment_id: str):
    """Retrieve a single comment by its id.

    For simplicity this builds the key as `COMMENT#<comment_id>` for both
    partition and sort key and queries the table.

    Args:
        comment_id: The comment object id to look up.

    Returns:
        The retrieved item as a dict if found, otherwise None.
        :param comment_id:
        :param post_id:
    """
    pk = sk = dynamo_db.generate_key(obj_type='COMMENT', obj_id=comment_id)
    return _table_client.get_item(hash_key=pk, sort_key=sk)


def delete_all_post_comments(post_id: str):
    return _table_client.delete_all_items()


def batch_create_post_comments(comments: list[Comment]):
    return _table_client.batch_write_items([c.model_dump(mode='json') for c in comments])


def get_post_comments(post_id: str, limit: int = 25):
    post_pk = dynamo_db.generate_key(obj_type='POST', obj_id=post_id)
    return _table_client.query_items_by_prefix(hash_key_value=post_pk, sort_key_prefix='COMMENT#', limit=limit)
