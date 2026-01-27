from fastapi import FastAPI
from mangum import Mangum

from src import logs
from src.amazon import param_store
from src.api.scrape.scrape_subreddit_posts import router as scrape_router
from src.api.v1.comment_api import router as comment_router
from src.api.v1.item_api import router as item_router
from src.api.v1.post_api import router as post_router

app = FastAPI()
environment = param_store.get_secret('ENVIRONMENT')
logger = logs.get_logger()
logger.info(f'Starting up ARM API in {environment}')

@app.get("/")
def read_root():
    return {"message": "Welcome to the Adrian Site API"}

app.include_router(item_router, prefix="/item", tags=["items"])
app.include_router(post_router, prefix="/post", tags=["posts"])
app.include_router(comment_router, prefix="/post/{post_id}/comment", tags=["comments"])
app.include_router(scrape_router, prefix="/scrape", tags=["scrape"])
handler = Mangum(app, lifespan="off")
