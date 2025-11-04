from fastapi import APIRouter

from src import decorators

router = APIRouter()


@router.get("/{item_id}")
@decorators.require_dev_environment
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
