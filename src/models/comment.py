import pydantic

from .base import ConfiguredModel


class Comment(ConfiguredModel):
    obj_type: str = 'COMMENT'
    pk: str = ''
    sk: str = ''
    author: str
    body_html: str
    parent_id: str
    permalink: str

    @pydantic.model_validator(mode='after')
    def validate_keys(self):
        if not self.pk:
            self.pk = self.generate_key(obj_type=self._get_parent_type(), obj_id=self.parent_id)
        if not self.sk:
            self.sk = self.generate_key(obj_type=self.obj_type, obj_id=self.obj_id)
        return self

    def _get_parent_type(self) -> str:
        obj_mapping = {
            'POST#': 'POST',
            'COMMENT#': 'COMMENT'
        }
        return obj_mapping[self.parent_id.split('#')[0]]