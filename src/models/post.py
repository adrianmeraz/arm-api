import pydantic
from .base import BaseDDBModel

class Post(BaseDDBModel):
    _type: str = "POST"
    _sk: str = pydantic.PrivateAttr(default=BaseDDBModel.generate_pk)
    author: str
    body_html: str
    category: str
    image_url: str
    is_locked: bool = False
    permalink: str
    title: str
