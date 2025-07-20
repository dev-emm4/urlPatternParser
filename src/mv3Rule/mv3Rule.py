from condition import Condition
from action import Action

class Mv3Rule:
    def __init__(self):
        self.id: int
        self.priority: int
        self.action: Action
        self.condition: Condition


