from .base import BaseDDBModel

class Post(BaseDDBModel):
    Type: str = "POST"
    Author: str
    BodyHtml: str
    Category: str
    ImageUrl: str
    IsLocked: bool = False
    Permalink: str
    Title: str
