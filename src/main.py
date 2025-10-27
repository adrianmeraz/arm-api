from fastapi import FastAPI
from mangum import Mangum

from src import logs
from src.api.scrape.scrape_subreddit_posts import router as scrape_router
from src.api.v1.item_api import router as items_router
from src.api.v1.post_api import router as posts_router

app = FastAPI()
logger = logs.get_logger()
logger.info("Starting up ARM API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Adrian Site API"}

app.include_router(items_router, prefix="/items", tags=["items"])
app.include_router(posts_router, prefix="/posts", tags=["posts"])
app.include_router(scrape_router, prefix="/scrape", tags=["scrape"])
handler = Mangum(app, lifespan="off")
