from figment import Aspect, action, before


def tell(self, msg):
    try:
        self.memory.append(msg)
    except AttributeError:
        self.memory = [msg]


def saw(self, msg):
    try:
        mems = self.memory
    except AttributeError:
        mems = []
    for mem in mems:
        if msg in mem:
            return True
    raise AssertionError('%r not found in %r' % (msg, mems))


class Visible(Aspect):
    """
    A simplified version of Positioned, from the example aspects. It doesn't do
    descriptor resolution (you have to use the entity ID).
    """

    @action(r'^l(?:ook)?(?: at)? (?P<descriptor>.+)')
    def look_at(event):
        target = event.actor.zone.get(event.descriptor)
        if not target:
            event.actor.tell('No such entity %r.' % event.descriptor)
            return

        yield 'before', event.actor.zone.all()
        if not event.prevented:
            event.actor.tell(target.desc)


class Colorful(Aspect):
    """An example aspect that includes state and actions."""

    def __init__(self, color='blue'):
        self.color = color

    def to_dict(self):
        return {'color': self.color}

    @action(r'^color(?: of)? (?P<descriptor>.+)')
    def color_of(event):
        target = event.actor.zone.get(event.descriptor)
        if not target:
            event.actor.tell('No such entity %r.' % event.descriptor)
            return

        if not target.has_aspect(Colorful):
            event.actor.tell("{0.Name} has no particular color.".format(target))
            return

        yield 'before', event.actor.zone.all()
        if not event.prevented:
            event.actor.tell('{0.Name} is {0.Colorful.color}.'.format(target))

    @action(r'^paint (?P<descriptor>.+) (?P<color>.+)')
    def paint(event):
        target = event.actor.zone.get(event.descriptor)
        if not target:
            event.actor.tell('No such entity %r.' % event.descriptor)
            return

        if not target.has_aspect(Colorful):
            event.actor.tell("{0.Name} cannot be painted.".format(target))
            return

        yield 'before', event.actor.zone.all()
        if not event.prevented:
            target.Colorful.color = event.color
            event.actor.tell('{0.Name} is now {0.Colorful.color}.'.format(target))


class BlackHole(Aspect):
    """An example aspect that overrides actions from another."""
    @before(Colorful.paint)
    def absorb_paint(self, event):
        if self.entity.id == event.descriptor:
            event.color = 'black'

    @before(Visible.look_at)
    def prevent_look_at(self, event):
        if self.entity.id == event.descriptor:
            event.actor.tell("You're unable to look directly at {0.name}.".format(self.entity))
            event.prevent_default()
