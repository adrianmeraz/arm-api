import datetime
import uuid

import pydantic
from pydantic import BaseModel

from src import logs

logger = logs.get_logger()


class ConfiguredModel(BaseModel):
    @staticmethod
    def now_timestamp() -> int:
        return int(datetime.datetime.now().timestamp())

    @staticmethod
    def generate_id() -> str:
        return uuid.uuid4().hex

    @staticmethod
    def generate_key(obj_type: str, obj_id: str) -> str:
        key = f'{obj_type.upper()}#{obj_id}'
        logger.info(f'Generated key: {key}')
        return key

    obj_id: str = pydantic.Field(default_factory=generate_id)
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
            self.pk = self.generate_key(obj_type=self.obj_type, obj_id=self.obj_id)
            logger.info(f'New PK: {self.pk}')
        return self
