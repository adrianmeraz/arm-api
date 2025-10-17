from .base import BaseDDBModel

class Post(BaseDDBModel):
    author: str
    body_html: str
    category: str
    image_url: str
    is_locked: bool = False
    permalink: str
    title: str
