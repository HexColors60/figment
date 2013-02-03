from schema import Aspect, Event, before
from . import Positioned
import random

class Psychic(Aspect):
    @before(Positioned.say)
    def prepeat(self, event):
        if self.entity.has_aspect(Positioned):
            self.entity.perform(Positioned.say, message=event.message)
