from fastapi import APIRouter
from pydantic import BaseModel

from src import decorators, logs
from src.scrape.scrape_subreddit_posts import ScrapeRequest

router = APIRouter()

logger = logs.get_logger()

class Request(BaseModel):
    subreddits: list[str]
    post_limit: int

@router.post("/subreddit-posts")
@decorators.require_dev_environment
async def scrape_subreddit_posts(request: Request):
    await ScrapeRequest(subreddits=request.subreddits, post_limit=request.post_limit).scrape()
    return True
