from condition import Condition
from action import Action

class Mv3Rule:
    def __init__(self, aId: int, aPriority: int, aAction: Action, aCondition: Condition):
        self.id: int = aId
        self.priority: int = aPriority
        self.action: Action = aAction
        self.condition: Condition = aCondition

    def to_dict(self):
        dictMv3Rule = {}

        for key, value in self.__dict__.items():
            if hasattr(value, 'to_dict'):
                dictMv3Rule[key] = value.to_dict()
            else:
                dictMv3Rule[key] = value

        return  dictMv3Rule


