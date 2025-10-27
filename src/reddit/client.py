import httpx

class RedditClient:
    _user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0'
    _ssl_context = httpx.create_ssl_context()

    def __init__(self, user_agent:str = None, proxy: str | None = None):
        self.user_agent = user_agent or self._user_agent
        self.base_url = "https://www.reddit.com"
        self.client = httpx.Client(
            base_url=self.base_url,
            headers={"User-Agent": self.user_agent},
            proxy=proxy,
            verify=self._ssl_context
        )
