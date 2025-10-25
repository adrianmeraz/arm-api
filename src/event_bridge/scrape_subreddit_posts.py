from src import logs
from src.amazon import dynamodb, param_store
from src.amazon.dynamo_db import DynamoDBClient
from src.reddit.client import RedditClient
from src.reddit.post_api import PostApi

logger = logs.get_logger()
table_name = param_store.get_secret('AWS_DYNAMO_DB_TABLE_NAME')
post_client = DynamoDBClient(dynamodb_client=dynamodb, table_name=table_name)

def lambda_handler(event, context):
    logger.info(f'event: {event}, context: {context}')
    post_limit = event.get('post_limit', 10)
    subreddits = event.get('subreddits', [])
    for subreddit in subreddits:
        response = scrape_subreddit_posts(subreddit=subreddit, post_limit=post_limit)
        # Placeholder for actual scraping logic
    return True

def scrape_subreddit_posts(subreddit: str, post_limit: int):
    logger.info(f'Scraping subreddit: {subreddit}')
    with RedditClient() as client:
        response = PostApi.get_subreddit_hot_posts(client, subreddit, limit=post_limit)

