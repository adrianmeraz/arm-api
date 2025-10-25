import httpx

from src.reddit.api import RedditApi
from src.reddit.client import RedditClient
from src.reddit.models.post_listing import PostListing


class Subreddit(RedditApi):
    @staticmethod
    def get_subreddit_hot_posts(client: RedditClient, subreddit: str, limit: int = 10) -> PostListing:
        url = f"{client.base_url}/r/{subreddit}/hot.json?limit={limit}"
        headers = {
            'User-Agent': client.user_agent
        }
        response = httpx.get(url, headers=headers)

        response.raise_for_status()
        return PostListing(response.json())
