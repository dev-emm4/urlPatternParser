from condition import Condition
from action import Action

class Mv3Rule:
    def __init__(self, aId: int, aPriority: int, aAction: Action, aCondition: Condition):
        self.id: int = aId
        self.priority: int = aPriority
        self.action: Action = aAction
        self.condition: Condition = aCondition


