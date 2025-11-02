import pydantic

from .base import ConfiguredModel
from pydantic import BaseModel

from ..amazon import dynamo_db


class Post(ConfiguredModel):
    obj_type: str = 'POST'
    pk: str = ''
    sk: str = ''
    author: str
    body_html: str
    category: str
    image_url: str
    is_locked: bool = False
    permalink: str
    title: str

    @pydantic.model_validator(mode='after')
    def validate_keys(self):
        if not self.pk:
            self.pk = dynamo_db.generate_key(obj_type=self.obj_type, obj_id=self.obj_id)
        if not self.sk:
            self.sk = self.pk
        return self


class PostOut(BaseModel):
    obj_id: str
    author: str
    body_html: str
    category: str
    image_url: str
    permalink: str
    title: str
