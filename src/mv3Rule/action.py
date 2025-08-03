class Action:
    def __init__(self, aType):
        self.type: str = aType

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}