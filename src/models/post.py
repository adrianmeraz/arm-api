import pydantic

from .base import BaseDDBModel


class Post(BaseDDBModel):
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
