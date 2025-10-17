from .base import BaseDDBModel

class Comment(BaseDDBModel):
    author: str
    body_html: str
    parent_id: str
    permalink: str
