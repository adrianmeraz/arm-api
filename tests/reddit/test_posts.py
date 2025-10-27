import json
import re
from importlib.resources import open_text

import httpx
import pytest
import respx

from src.reddit.client import RedditAsyncClient
from src.reddit.post_api import PostApi
from tests.fixtures import ROOT_RESOURCE_PATH


@respx.mock
async def test_get_subreddit_hot_posts_success():
    client = RedditAsyncClient()
    subreddit = "space"
    limit = 2

    # load fixture
    with open_text(ROOT_RESOURCE_PATH, 'subreddit_posts_hot.json') as text:
        data_json = json.loads(text.read())

    route = respx.route(
        method='GET',
    ).mock(
        return_value=httpx.Response(
            headers=None,
            status_code=200,
            json=data_json,
        )
    )

    result = await PostApi.get_subreddit_hot_posts(client, subreddit, limit=limit)
    posts = result.data.children
    post_2 = posts[1]

    assert route.call_count == 1
    assert len(posts) >= 10

    assert post_2.author == 'ChiefLeef22'
    assert post_2.id == '1oe1qg2'
    assert post_2.is_active is True
    assert post_2.is_video is False
    assert post_2.num_comments == 316
    assert post_2.preview.all_image_sources == ['https://external-preview.redd.it/Xw7GdwEySMM9cMGT5SAFvSgWpO1nFUlSHmsiosX8PcI.jpeg?auto=webp&amp;s=32d4ad9f84ebb4ad15dd91a4e2fbbfa6c7ce9646']
    assert post_2.url == 'https://arstechnica.com/space/2025/10/texas-lawmakers-double-down-on-discovery-call-for-doj-investigation-into-smithsonian/'
    assert post_2.score == 5948
    assert post_2.subreddit == 'space'
    assert post_2.ups == 5948

@respx.mock
def test_get_subreddit_hot_posts_http_error():
    client = RedditAsyncClient()
    subreddit = "space"

    # mock a 500 response
    route = respx.get(re.compile(rf"{re.escape(str(client.base_url))}/r/{subreddit}/hot\.json.*")).mock(
        return_value=httpx.Response(500, json={"message": "internal error"})
    )

    with pytest.raises(httpx.HTTPStatusError):
        PostApi.get_subreddit_hot_posts(client, subreddit)

    assert route.called

