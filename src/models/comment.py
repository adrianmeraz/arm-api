import pydantic

from .base import ConfiguredModel
from ..amazon import dynamo_db


class Comment(ConfiguredModel):
    obj_type: str = 'COMMENT'
    pk: str = ''
    sk: str = ''
    author: str
    body_html: str
    parent_id: str
    post_id: str
    permalink: str

    @pydantic.model_validator(mode='after')
    def validate_keys(self):
        if not self.pk:
            self.pk = dynamo_db.generate_key(obj_type='POST', obj_id=self.parent_id)
        if not self.sk:
            self.sk = dynamo_db.generate_key(obj_type=self.obj_type, obj_id=self.obj_id)
        return self
