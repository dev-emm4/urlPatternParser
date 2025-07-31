from typing import List

from src.mv3Rule.action import Action
from src.mv3Rule.mv3Rule import Condition
from src.mv3Rule.mv3Rule import Mv3Rule
from unFormattedRuleOptionValidator import UnFormattedRuleOptionValidator


class Mv3RuleFactory:
    def createMv3Rule(self, aUnformattedRule: str, aId: int) -> Mv3Rule:
        condition: Condition = self._instantiateCondition(aUnformattedRule)

        if self._isUnformattedRuleBlocking(aUnformattedRule):
            action: Action = self._instantiateAction('block')
            mv3Rule: Mv3Rule = self._instantiateMv3Rule(aId, 1, action, condition)
            return mv3Rule
        else:
            action: Action = self._instantiateAction('allow')
            mv3Rule: Mv3Rule = self._instantiateMv3Rule(aId, 2, action, condition)
            return mv3Rule

    def _instantiateCondition(self, aUnformattedRule: str) -> Condition:
        condition: Condition = Condition()

        if self._doesUnformattedRuleHaveOption(aUnformattedRule):
            pattern: str = self._retrievePatternIn(aUnformattedRule)
            pattern = self._removeAllowSymbolFromPattern(pattern)

            self._setPatternInCondition(pattern, condition)
            option: str = self._retrieveOptionIn(aUnformattedRule)

            if self._isOptionAList(option):
                optionList: List[str] = self._splitOptions(option)
                self._setConditionParameterUsingOptionList(condition, optionList)
            else:
                self._setDomainTypeInCondition(condition, option)
                self._setInitiatorDomainInCondition(condition, option)
                self._setResourceTypeInCondition(condition, option)

            return condition
        else:
            pattern: str = aUnformattedRule
            self._setPatternInCondition(pattern, condition)
            return condition

    def _removeAllowSymbolFromPattern(self, aPattern: str):
        if aPattern.startswith('@@'):
            return aPattern[2:]
        return aPattern

    def _doesUnformattedRuleHaveOption(self, aUnformattedRule: str) -> bool:
        if '$' in aUnformattedRule:
            return True
        return False

    def _retrievePatternIn(self, aUnformattedRule: str) -> str:
        pattern: str = aUnformattedRule.split('$', 1)[0]
        return pattern

    def _setPatternInCondition(self, aPattern: str, aCondition: Condition):
        if self._isPatternregexFilter(aPattern):
            aCondition.setRegexFilter(aPattern)
        else:
            aCondition.setUrlFilter(aPattern)

    def _isPatternregexFilter(self, aPattern: str):
        if aPattern.startswith('/') and aPattern.endswith('/'):
            return True
        else:
            return False

    def _retrieveOptionIn(self, aUnformattedRule: str) -> str:
        option: str = aUnformattedRule.split('$', 1)[1]
        return option

    def _isOptionAList(self, aOption: str) -> bool:
        if ',' in aOption:
            return True
        return False

    def _splitOptions(self, aOption: str) -> List[str]:
        return aOption.split(',')

    def _setConditionParameterUsingOptionList(self, aCondition: Condition, aOptionList: List[str]):
        for option in aOptionList:
            self._setDomainTypeInCondition(aCondition, option)
            self._setInitiatorDomainInCondition(aCondition, option)
            self._setResourceTypeInCondition(aCondition, option)

    def _setDomainTypeInCondition(self, aCondition: Condition, aOption: str):
        optionValidator: UnFormattedRuleOptionValidator = UnFormattedRuleOptionValidator()

        if not optionValidator.optionIsAValidDomainType(aOption):
            return
        if not aCondition.isDomainTypeNone():
            raise Exception('domain Type conflict')

        aCondition.setDomainType(aOption)

    def _setInitiatorDomainInCondition(self, aCondition: Condition, aOption: str):
        optionValidator: UnFormattedRuleOptionValidator = UnFormattedRuleOptionValidator()

        if not optionValidator.optionIsAInitiatorDomain(aOption):
            return
        if aCondition.isInitiatorDomainSet():
            raise Exception('double domain found in rule')

        newInitiatorDomain: str = self._cleanInitiatorDomain(aOption)

        if self._isInitiatorDomainAList(newInitiatorDomain):
            initiatorDomainList: List[str] = self._splitInitiatorDomains(newInitiatorDomain)
            aCondition.setInitiatorDomain(initiatorDomainList)
        else:
            initiatorDomainList: List[str] = [newInitiatorDomain]
            aCondition.setInitiatorDomain(initiatorDomainList)

    def _cleanInitiatorDomain(self, aInitiatorDomain: str) -> str:
        cleanInitiatorDomain: str = aInitiatorDomain.split('domain=', 1)[1]
        return cleanInitiatorDomain

    def _isInitiatorDomainAList(self, aInitiatorDomain: str) -> str:
        if '|' in aInitiatorDomain:
            return True
        return False

    def _splitInitiatorDomains(self, aInitiatorDomain: str) -> list[str]:
        return aInitiatorDomain.split('|')

    def _setResourceTypeInCondition(self, aCondition: Condition, aOption: str):
        optionValidator: UnFormattedRuleOptionValidator = UnFormattedRuleOptionValidator()

        if not optionValidator.optionIsAValidResourceType(aOption):
            return
        aCondition.setResourceType(aOption)

    def _isUnformattedRuleBlocking(self, aUnformattedRule: str) -> bool:
        if aUnformattedRule.startswith('@@'):
            return False
        return True

    def _instantiateAction(self, aType) -> Action:
        return Action(aType)

    def _instantiateMv3Rule(self, aId: int, aPriority: int, aAction: Action, aCondition: Condition) -> Mv3Rule:
        return Mv3Rule(aId, aPriority, aAction, aCondition)
