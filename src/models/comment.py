from .base import ConfiguredModel

class Comment(ConfiguredModel):
    author: str
    body_html: str
    parent_id: str
    permalink: str
