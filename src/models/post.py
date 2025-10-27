import pydantic

from .base import ConfiguredModel
from pydantic import BaseModel


class Post(ConfiguredModel):
    obj_type: str = "POST"
    sk: str = ''
    author: str
    body_html: str
    category: str
    image_url: str
    is_locked: bool = False
    permalink: str
    title: str

    @pydantic.model_validator(mode='after')
    def validate_sk(self):
        if not self.sk and self.pk:
            self.sk = self.pk
        return self


class PostOut(BaseModel):
    author: str
    body_html: str
    category: str
    image_url: str
    permalink: str
    title: str
