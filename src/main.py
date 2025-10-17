from fastapi import FastAPI
from mangum import Mangum

from src.api.v1.items import router as items_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}

app.include_router(items_router, prefix="/items", tags=["items"])
handler = Mangum(app, lifespan="off")
