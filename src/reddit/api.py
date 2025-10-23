import httpx

class RedditClient:
    _user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0'

    def __init__(self, user_agent=None):
        self.user_agent = user_agent or self._user_agent
        self.base_url = "https://www.reddit.com"

    def get_subreddit_posts(self, subreddit, limit=10):
        headers = {"User-Agent": self.user_agent}
        url = f"{self.base_url}/r/{subreddit}/hot.json?limit={limit}"
        response = httpx.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
