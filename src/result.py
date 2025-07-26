from typing import List
from src.mv3Rule.mv3Rule import Mv3Rule

class Result:
    def __init__(self, aMv3RuleList: List[Mv3Rule], aUnresolvedRuleList: List[str]):
        self.mv3Rules: List[Mv3Rule] = aMv3RuleList
        self.unresolvedRules: List[str] = aUnresolvedRuleList