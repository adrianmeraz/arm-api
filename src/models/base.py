import uuid

import pydantic
from pydantic import BaseModel


class BaseDDBModel(BaseModel):
    Id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4)
    Type: str
    PK: str
    SK: str
    CreatedAt: str
    CreatedBy: str
    ModifiedAt: str
    ModifiedBy: str
    ExpiresAt: int
    IsDeleted: bool = True

    @classmethod
    def create_pk(cls, _type: str, _id: str) -> str:
        return f'{_type}#{_id}'

    def generate_pk(self):
        return f'{self.Type}#{self.Id}'