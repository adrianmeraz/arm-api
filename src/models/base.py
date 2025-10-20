import datetime
import logging
import uuid

import pydantic
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class BaseDDBModel(BaseModel):
    @staticmethod
    def now_timestamp() -> datetime.datetime:
        return datetime.datetime.now()

    def generate_pk(self):
        pk = f'{self.Type}#{self.Id}'
        logger.info(f'Generated PK: {pk}')
        return pk

    @classmethod
    def create_pk(cls, _type: str, _id: str) -> str:
        return f'{_type}#{_id}'

    _id: uuid.UUID = pydantic.PrivateAttr(default_factory=uuid.uuid4)
    _type: str = pydantic.PrivateAttr()
    _pk: str = pydantic.PrivateAttr(default=generate_pk)
    _sk: str = pydantic.PrivateAttr()
    _created_at: str = pydantic.PrivateAttr(default_factory=now_timestamp)
    _created_by: str = pydantic.PrivateAttr()
    _modified_at: str = pydantic.PrivateAttr(default_factory=now_timestamp)
    _modified_by: str = pydantic.PrivateAttr()
    _expires_at: int | None = pydantic.PrivateAttr(default=None)
    _is_deleted: bool = pydantic.PrivateAttr(default=False)
