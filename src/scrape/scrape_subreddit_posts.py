from src import logs
from src.adapters.post import PostAdapter
from src.data import post_data
from src.models.post import Post
from src.reddit.client import RedditAsyncClient
from src.reddit.models.post import Post as RedditPost
from src.reddit.models.post_listing import PostListing as RedditPostListing
from src.reddit.post_api import PostApi

logger = logs.get_logger()


class ScrapeRequest:
    def __init__(self, subreddits: list[str], post_limit: int = 10):
        self.subreddits = subreddits
        self.post_limit = post_limit

    async def scrape(self):
        for subreddit in self.subreddits:
            response: RedditPostListing = await self._scrape_posts(subreddit=subreddit)
            r_posts: list[RedditPost] = response.data.children
            posts: list[Post] = [PostAdapter.to_ddb_post(r_post) for r_post in r_posts]
            post_data.batch_create_posts(posts)

        return True

    async def _scrape_posts(self, subreddit: str):
        logger.info(f'Scraping subreddit: {subreddit}')
        async with RedditAsyncClient() as client:
            return await PostApi.get_subreddit_hot_posts(client, subreddit=subreddit, limit=self.post_limit)
