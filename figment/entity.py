import collections.abc
import inspect
import json

from figment.logger import log


class ComponentStore:
    def __init__(self, entity):
        self.entity = entity
        self.components = {}

    def add(self, components):
        if not isinstance(components, collections.abc.Iterable):
            components = [components]

        for component in components:
            component_name = component.__class__.__name__
            setattr(self.entity, component_name, component)
            component.attach(self.entity)
            self.components[component_name] = component

            if self.entity.zone:
                self.entity.zone.entities_by_component_name.setdefault(
                    component_name, set()
                ).add(self.entity)

        if self.entity.zone and self.entity.ticking:
            self.entity.zone.ticking_entities.add(self.entity)

    def remove(self, component_names):
        if isinstance(component_names, str) or not isinstance(
            component_names, collections.abc.Iterable
        ):
            component_names = [component_names]

        for component_name in component_names:
            if inspect.isclass(component_name):
                component_name = component_name.__name__
            getattr(self.entity, component_name).detach()
            delattr(self.entity, component_name)
            self.components.pop(component_name, None)

            if self.entity.zone:
                self.entity.zone.entities_by_component_name[component_name].remove(
                    self.entity
                )

        if (
            self.entity.zone
            and self.entity in self.entity.zone.ticking_entities
            and not self.entity.ticking
        ):
            self.entity.zone.ticking_entities.remove(self.entity)

    def has(self, component_names):
        if isinstance(component_names, str) or not isinstance(
            component_names, collections.abc.Iterable
        ):
            component_names = [component_names]

        for component_name in component_names:
            if inspect.isclass(component_name):
                component_name = component_name.__name__
            if component_name not in self.components:
                return False
        return True

    def purge(self):
        self.remove(list(self.components.keys()))

    def __iter__(self):
        return self.components.values().__iter__()


class Entity:
    def __init__(self, id=None, zone=None, hearing=False, mode=None):
        self.id = id
        self.mode = mode
        self.components = ComponentStore(self)
        self.zone = zone
        self.hearing = hearing

    def __eq__(self, other):
        if isinstance(other, Entity):
            return self.id == other.id
        return NotImplemented

    def __ne__(self, other):
        equal = self.__eq__(other)
        return NotImplemented if equal is NotImplemented else not equal

    def __hash__(self):
        return hash(self.id)

    @property
    def ticking(self):
        return any(c.ticking for c in self.components)

    def to_dict(self):
        if self.mode:
            mode_dict = self.mode.to_dict()
            mode_dict["__class__"] = self.mode.__class__.__name__
        else:
            mode_dict = None

        return {
            "id": self.id,
            "mode": mode_dict,
            "hearing": self.hearing,
            "components": dict(
                (c.__class__.__name__, c.to_dict()) for c in self.components
            ),
        }

    @classmethod
    def from_dict(cls, dict_, zone):
        entity = cls(id=dict_["id"], hearing=dict_["hearing"])
        zone.add(entity)
        entity.attach_from_dict(dict_)
        return entity

    def attach_from_dict(self, dict_):
        mode_dict = dict_.get("mode", {})
        if mode_dict:
            mode_name = mode_dict.pop("__class__")
            self.mode = self.zone.modes[mode_name].from_dict(mode_dict)
        else:
            self.mode = None

        components = []
        for component_name, component_dict in dict_.get("components", {}).items():
            component = self.zone.components[component_name].from_dict(component_dict)
            components.append(component)

        self.components.add(components)

    def is_(self, *args, **kwargs):
        return self.components.has(*args, **kwargs)

    def perform(self, *args, **kwargs):
        if self.mode:
            self.mode.perform(self, *args, **kwargs)
        else:
            log.warn(
                "Entity [%s] tried to perform %r, but it has no mode"
                % (self.id, (args, kwargs))
            )

    def tell(self, message):
        """Send text to this entity."""
        if self.hearing:
            self.zone.send_message(self.id, json.dumps(message))
