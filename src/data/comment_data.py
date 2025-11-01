from src.amazon import dynamodb, param_store
from src.amazon.dynamo_db import DynamoDBClient
from src.models.comment import Comment

_table_name = param_store.get_secret('AWS_DYNAMO_DB_TABLE_NAME')
_table_client = DynamoDBClient(dynamodb_client=dynamodb, table_name=_table_name)


def create_comment(comment: Comment):
    return _table_client.create_item(comment.model_dump(mode='json'))


def delete_comment(comment_pk: str):
    return _table_client.delete_item(hash_key=comment_pk, sort_key=comment_pk)


def delete_all_comments():
    return _table_client.delete_all_items()


def batch_create_comments(comments: list[Comment]):
    return _table_client.batch_write_items([c.model_dump(mode='json') for c in comments])


def get_all_comments():
    return _table_client.get_all_table_items()

