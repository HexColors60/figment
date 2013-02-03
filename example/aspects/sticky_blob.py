from schema import Aspect, before
from . import Positioned
import random

class StickyBlob(Aspect):
    """A difficult-to-drop item."""
    def __init__(self, stickiness=0.5):
        self.stickiness = stickiness

    def to_dict(self):
        return {'stickiness': self.stickiness}

    @classmethod
    def from_dict(cls, dict_):
        return cls(stickiness=dict_['stickiness'])

    @before(Positioned.drop)
    def stick(self, event):
        if self.entity == event.target and random.random() < self.stickiness:
            event.actor.tell('You try to drop {0.name}, but it sticks to your hand.'.format(self.entity))
            event.prevent_default()
