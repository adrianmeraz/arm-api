import datetime
import uuid
from typing import Any, Dict

import pydantic
from pydantic import BaseModel

from src import logs

logger = logs.get_logger()


class BaseDDBModel(BaseModel):
    @staticmethod
    def now_timestamp() -> int:
        return int(datetime.datetime.now().timestamp())

    def generate_pk(self):
        pk = f'{self.obj_type}#{self.obj_id}'
        logger.info(f'Generated PK: {pk}')
        return pk

    @classmethod
    def create_pk(cls, obj_type: str, obj_id: uuid.uuid4) -> str:
        return f'{obj_type}#{obj_id}'

    obj_id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4)
    obj_type: str = ''
    pk: str = ''
    sk: str = ''
    created_at_utc: int = pydantic.Field(default_factory=now_timestamp)
    created_by: str = ''
    modified_at_utc: int = pydantic.Field(default_factory=now_timestamp)
    modified_by: str = ''
    expires_at: int | None = None
    is_deleted: bool = False

    @pydantic.model_validator(mode='after')
    def validate_pk(self):
        if self.pk == "" and all([self.obj_type, self.obj_id]):
            self.pk = self.create_pk(obj_type=self.obj_type, obj_id=self.obj_id)
            logger.info(f'New PK: {self.pk}')
        return self
