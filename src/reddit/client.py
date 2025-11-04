import httpx
from httpx import AsyncClient

class RedditAsyncClient(AsyncClient):
    _user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0'
    _ssl_context = httpx.create_ssl_context()

    def __init__(self, user_agent:str = None, proxy: str | None = None):
        super().__init__(
            base_url="https://www.reddit.com",
            headers={"User-Agent": user_agent or self._user_agent},
            proxy=proxy,
            verify=self._ssl_context
        )
