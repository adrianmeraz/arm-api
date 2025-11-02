from src import logs
from src.amazon import dynamodb, param_store
from src.amazon.dynamo_db import DynamoDBClient
from src.models.post import Post

_table_name = param_store.get_secret('AWS_DYNAMO_DB_TABLE_NAME')
_table_client = DynamoDBClient(dynamodb_client=dynamodb, table_name=_table_name)
logger = logs.get_logger()

def create_post(post: Post):
    """Create a post record in DynamoDB.

    The given `post` model is serialized to a JSON-compatible dict and sent
    to the DynamoDB client.

    Args:
        post: A `Post` model instance to persist.

    Returns:
        The item that was written (the same dict that was passed to the
        DynamoDB client) or whatever the underlying client returns on
        success.

    Raises:
        src.exceptions.DDBException: If the underlying DynamoDB client
            encounters an error while writing the item.
    """
    return _table_client.create_item(post.model_dump(mode='json'))

def delete_post(post_id: str):
    """Delete a single post from DynamoDB by its primary key.

    Args:
        post_id: The partition key (and sort key) of the post to delete. The
            functions in this module commonly use generated keys of the form
            "POST#<id>".

    Returns:
        The raw response returned by the DynamoDB client's `delete_item`
        operation.
    """
    pk = sk = Post.generate_key(obj_type='POST', obj_id=post_id)
    logger.info(f'Deleting post with PK: {pk}, SK: {sk}')
    return _table_client.delete_item(hash_key=post_id, sort_key=post_id)

def delete_all_posts():
    """Delete all posts from the DynamoDB table.

    This scans the table and issues batch deletes for every item found. Use
    with caution in production as it will remove all data from the table.

    Returns:
        The result of the DynamoDB client's delete-all operation (usually
        None) or raises an exception on failure.
    """
    logger.info(f'Deleting all posts')
    return _table_client.delete_all_items()

def get_post(post_id: str):
    """Retrieve a single post by its object id.

    This builds the DynamoDB key using the model's key generator so callers
    can pass the original post id (e.g. reddit id) rather than the full PK.

    Args:
        post_id: The object identifier for the post (not the full PK).

    Returns:
        The retrieved item as a dict if found, or `None` if the item does
        not exist.
    """
    pk = sk = Post.generate_key(obj_type='POST', obj_id=post_id)
    return _table_client.get_item(hash_key=pk, sort_key=sk)

def batch_create_posts(posts: list[Post]):
    """Write multiple posts to DynamoDB in a batch operation.

    Args:
        posts: A list of `Post` model instances to persist.

    Returns:
        The response from the batch write operation. Depending on the
        underlying client, unprocessed items may be returned.
    """
    return _table_client.batch_write_items([post.model_dump(mode='json') for post in posts])

def get_all_posts():
    """Fetch all posts from the DynamoDB table.

    Returns:
        A list of items (each a dict) representing all posts in the table.
    """
    return _table_client.get_all_table_items()
