from src.reddit.api import RedditApi
from src.reddit.client import RedditAsyncClient
from src.reddit.models.post_listing import PostListing


class Subreddit(RedditApi):
    @staticmethod
    async def get_subreddit_hot_posts(client: RedditAsyncClient, subreddit: str, limit: int = 10) -> PostListing:
        url = f"{client.base_url}/r/{subreddit}/hot.json?limit={limit}"
        response = await client.get(url, headers=client.headers)

        response.raise_for_status()
        return PostListing(response.json())
