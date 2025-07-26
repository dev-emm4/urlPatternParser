from typing import List
from src.mv3Rule.mv3Rule import Mv3Rule
from src.mv3Rule.mv3Rule import Condition
from src.mv3Rule.action import Action
from src.result import Result

class UrlToMv3FilterTransformer:
    def __init__(self):
        self.unResolvedRules: List[str] = []
        self.mv3Rules: List[Mv3Rule] = []
        self.id = 0

    def transform(self, unFormattedRules:List[str]) -> Result:
        if self._isListEmpty(unFormattedRules):
            return self._instantiateResult()

        for unFormattedRule in unFormattedRules:
            self._createAndAppendMv3RuleToMv3RuleList(unFormattedRule)
            self._incrementId()
        result: Result = self._instantiateResult()
        self._reset()
        return result

    def _isListEmpty(self, aList):
        if len(aList) == 0:
            return True
        return False

    def _instantiateResult(self) -> Result:
        return Result(self.mv3Rules, self.unResolvedRules)

    def _createAndAppendMv3RuleToMv3RuleList(self, aUnformattedRule: str):
        try:
            condition: Condition = self._instantiateCondition(aUnformattedRule)
            if self._isUnformattedRuleBlocking(aUnformattedRule):
                action: Action = self._instantiateAction('block')
                mv3Rule: Mv3Rule = self._instantiateMv3Rule(1, action, condition)
                self.mv3Rules.append(mv3Rule)
            else:
                action: Action = self._instantiateAction('allow')
                mv3Rule: Mv3Rule = self._instantiateMv3Rule(2, action, condition)
                self.mv3Rules.append(mv3Rule)
        except Exception():
            self.unResolvedRules.append(aUnformattedRule)

    def _instantiateCondition(self, aUnformattedRule: str) -> Condition:
        condition: Condition = Condition()
        if self._doesUnformattedRuleHaveOption(aUnformattedRule):
            pattern: str = self._retrievePatternIn(aUnformattedRule)
            self._registerPatternInCondition(pattern, condition)
            option: str = self._retrieveOptionIn(aUnformattedRule)

            if self._isOptionAList(option):
                optionList: List[str] = self._createOptionListFrom(option)
                self._setConditionParameterUsingOptionList(condition, optionList)
            else:
                self._setConditionParameterUsingOption(condition, option)

            return condition
        else:
            pattern: str = aUnformattedRule
            self._registerPatternInCondition(pattern, condition)
            return condition

    def _doesUnformattedRuleHaveOption(self, aUnformattedRule: str) -> bool:
        if '$' in aUnformattedRule:
            return True
        return False

    def _retrievePatternIn(self, aUnformattedRule: str) -> str:
        pattern: str = aUnformattedRule.split('$', 1)[0]
        return pattern

    def _registerPatternInCondition(self, aPattern: str, aCondition: Condition):
        if self._isPatternregexFilter(aPattern):
            aCondition.regexFilter = aPattern
        else:
            aCondition.urlFilter = aPattern

    def _isPatternregexFilter(self, aPattern: str):
        if aPattern.startswith('/') and aPattern.endswith('/'):
            return True
        else:
            return  False

    def _retrieveOptionIn(self, aUnformattedRule: str) -> str:
        option: str = aUnformattedRule.split('$', 1)[1]
        return option

    def _isOptionAList(self, aOption: str) -> bool:
        if ',' in aOption:
            return True
        return False

    def _createOptionListFrom(self, aOption: str) -> List[str]:
        return aOption.split(',')

    # TODO implement register option in condition
    def _setConditionParameterUsingOptionList(self, aCondition: Condition, aOptionList: List[str]):
        pass

    def _setConditionParameterUsingOption(self, aCondition: Condition, aOption: str):
        pass

    def _isUnformattedRuleBlocking(self, aUnformattedRule: str) -> bool:
        if aUnformattedRule.startswith('@@'):
            return False
        return True

    def _instantiateAction(self, aType) -> Action:
        return Action(aType)

    def _instantiateMv3Rule(self, aPriority: int, aAction: Action, aCondition: Condition) -> Mv3Rule:
        return Mv3Rule(self.id, aPriority, aAction, aCondition)

    def _incrementId(self):
        self.id =+ 1

    def _reset(self):
        self.id = 0
        self.mv3Rules = []
        self.unResolvedRules = []