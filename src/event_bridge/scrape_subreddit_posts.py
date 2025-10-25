from src import logs
from src.reddit.post_api import PostApi
from src.reddit.client import RedditClient

logger = logs.get_logger()

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

