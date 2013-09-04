from figment import Aspect, action
from . import Positioned


class Usable(Aspect):
    """Provides a 'use' hook for entities."""

    @action(r'^use (?P<descriptor>.+)$')
    def use(event):
        if not event.actor.has_aspect(Positioned):
            event.actor.tell("You're unable to do that.")
            return

        event.target = event.actor.Positioned.pick_nearby_inventory(event.descriptor)
        if not event.target:
            return

        yield 'before'
        if not event.prevented:
            event.actor.tell("You can't use that.")

    @action(r'^use (?P<item_descriptor>.+) on (?P<target_descriptor>.+)')
    def use_on(event):
        if not event.actor.has_aspect(Positioned):
            event.actor.tell("You're unable to do that.")
            return

        event.item = event.actor.Positioned.pick_nearby_inventory(event.item_descriptor)
        if not event.item:
            return

        event.target = event.actor.Positioned.pick_nearby_inventory(event.target_descriptor)
        if not event.target:
            return

        yield 'before'
        if not event.prevented:
            event.actor.tell('Nothing happens.')
