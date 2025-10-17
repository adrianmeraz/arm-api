from pydantic import BaseModel

class BaseDDBModel(BaseModel):
    created_utc: str
    id: str
    is_deleted: bool = True
