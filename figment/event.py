class Event(object):
    def __init__(self, **kwargs):
        self.action = None
        self.actor = None
        self.prevented = False
        self.__dict__.update(kwargs)

    # This is probably considered unpythonic, but it makes the event API easier
    # to use, so I'm doin' it
    def __getattr__(self, key):
        return None

    def prevent_default(self):
        self.prevented = True
        # TODO: this is too specific to the before hook
        # How would someone "prevent" a custom hook?