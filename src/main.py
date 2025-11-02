from fastapi import FastAPI
from mangum import Mangum

from src import logs
from src.amazon import param_store
from src.api.scrape.scrape_subreddit_posts import router as scrape_router
from src.api.v1.comment_api import router as comments_router
from src.api.v1.item_api import router as items_router
from src.api.v1.post_api import router as posts_router

app = FastAPI()
environment = param_store.get_secret('ENVIRONMENT')
logger = logs.get_logger()
logger.info(f'Starting up ARM API in {environment}')

@app.get("/")
def read_root():
    return {"message": "Welcome to the Adrian Site API"}

app.include_router(items_router, prefix="/items", tags=["items"])
app.include_router(posts_router, prefix="/posts", tags=["posts"])
app.include_router(comments_router, prefix="/comments", tags=["comments"])
app.include_router(scrape_router, prefix="/scrape", tags=["scrape"])
handler = Mangum(app, lifespan="off")
