from figment import Component
from figment.utils import upper_first


class Named(Component):
    """Holds human-readable identifying info for an entity."""
    def __init__(self, name=None, desc=None):
        self.name = name
        self.desc = desc

    @property
    def Name(self):
        return upper_first(self.name)

    def to_dict(self):
        return {
            'name': self.name,
            'desc': self.desc,
        }

    @classmethod
    def from_dict(cls, dict_):
        return cls(
            name=dict_['name'],
            desc=dict_['desc'],
        )
