from typing import List
from src.mv3Rule.mv3Rule import Mv3Rule

class Result:
    def __init__(self):
        self.invalidUnFormattedRule: List[str] = []
        self.invalidMv3Rule: List[Mv3Rule] = []
        self.validMv3Rule: List[Mv3Rule] = []

    def setInvalidUnFormattedRule(self, aUnFormattedRule: str):
        self.invalidUnFormattedRule.append(aUnFormattedRule)

    def setInvalidMv3Rule(self, aMv3Rule: Mv3Rule):
        self.invalidMv3Rule.append(aMv3Rule)

    def setValidMv3Rule(self, aMv3Rule: Mv3Rule):
        self.validMv3Rule.append(aMv3Rule)
