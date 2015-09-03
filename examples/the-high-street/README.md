# The High Street

An example Figment world set along a fictitious city street.

## Components

This world includes several components that can be reused or adapted for your own purposes.

- **Position** is responsible for describing the spatial (hierarchical) relationship between entities. It handles much of the core functionality you'd expect from a MUD related to moving around, looking at, and taking and dropping things -- as well as whether or not actions taken by one entity can be heard by another.
- **Dark** overrides `Position.look` for any entity contained by a Dark entity, replacing the usual output with a "it's too dark" message.
- **Emotes** allows entities to emit a textual description of them performing an action, much like the `/me` command would on IRC.
- **Pest**, **ShoosPests**, and **Bird** are components for making entities act like, or react to, certain kinds of animals.
- **Important** prevents an entity from being dropped or taken.
- **Psychic** entities will say the same words as you... before you say them.
- **Speaking** provides a base for conversations, though it's unused at present.
- **StickyBlob** is a silly example of an entity that will randomly fail to be dropped.
- **Usable** provides hooks for using entities and using entities on other entities.
- **Wandering** entities will meander randomly between the specified rooms.