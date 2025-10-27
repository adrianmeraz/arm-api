from fastapi import FastAPI
from mangum import Mangum

from src import logs
from src.api.v1.api_items import router as items_router
from src.api.v1.api_posts import router as posts_router

app = FastAPI()
logger = logs.get_logger()
logger.info("Starting up ARM API")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

app.include_router(items_router, prefix="/items", tags=["items"])
app.include_router(posts_router, prefix="/posts", tags=["posts"])
handler = Mangum(app, lifespan="off")
