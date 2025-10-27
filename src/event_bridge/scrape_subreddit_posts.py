from src import logs
from src.scrape.scrape_subreddit_posts import ScrapeRequest

logger = logs.get_logger()

async def lambda_handler(event, context):
    logger.info(f'event: {event}, context: {context}')
    post_limit = event.get('post_limit', 10)
    subreddits = event.get('subreddits', [])
    await ScrapeRequest(subreddits=subreddits, post_limit=post_limit).scrape()
