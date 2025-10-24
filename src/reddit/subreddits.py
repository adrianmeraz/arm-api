import httpx

from src.reddit.api import RedditApi
from src.reddit.client import RedditClient


class Subreddit(RedditApi):
    @staticmethod
    def get_subreddit_hot_posts(client: RedditClient, subreddit: str, limit: int = 10):
        url = f"{client.base_url}/r/{subreddit}/hot.json?limit={limit}"
        headers = {'User-Agent': client.user_agent}
        response = httpx.get(url, headers=headers)

        response.raise_for_status()
        return response.json()
