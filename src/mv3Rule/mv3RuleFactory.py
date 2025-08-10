import re
from typing import List

from error import ParsingError
from .action import Action
from .condition import Condition
from .mv3Rule import Mv3Rule
from unFormattedRuleOptionValidator import UnFormattedRuleOptionValidator


class Mv3RuleFactory:
    def __init__(self):
        self.optionValidator: UnFormattedRuleOptionValidator = UnFormattedRuleOptionValidator()

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
        pattern: str = self._extractPatternFromUnformattedRule(aUnformattedRule)

        self._setRegexFilterInCondition(condition, pattern)
        self._setUrlFilterInCondition(condition, pattern)

        if not self._doesOptionExistInUnformattedRule(aUnformattedRule):
            return condition

        option: str = self._extractOptionFrom(aUnformattedRule)

        if self._isOptionAList(option):
            optionList: List[str] = self._splitOptions(option)
            self._setConditionUsingOptionList(condition, optionList)
        else:
            self._setDomainTypeInCondition(condition, option)
            self._setInitiatorDomainInCondition(condition, option)
            self._setResourceTypeInCondition(condition, option)
            self._activateUrlFilterCaseSensitiveInCondition(condition, option)

        return condition

    def _extractPatternFromUnformattedRule(self, aUnformattedRule: str) -> str:
        if self._doesOptionExistInUnformattedRule(aUnformattedRule):
            pattern: str = aUnformattedRule.split('$', 1)[0]
            pattern = self._removeAllowSymbolFromPattern(pattern)
            return pattern
        else:
            pattern: str = aUnformattedRule
            pattern = self._removeAllowSymbolFromPattern(pattern)
            return pattern

    def _doesOptionExistInUnformattedRule(self, aUnformattedRule: str) -> bool:
        if '$' in aUnformattedRule:
            return True
        return False

    def _removeAllowSymbolFromPattern(self, aPattern: str):
        if aPattern.startswith('@@'):
            return aPattern[2:]
        return aPattern

    def _setRegexFilterInCondition(self, aCondition: Condition, aPattern: str):
        if not self._isPatternRegexFilter(aPattern):
            return

        regexFilter: str = self._removeForwardSlash(aPattern)

        self._validateRegexFilter(regexFilter)
        aCondition.setRegexFilter(regexFilter)

    def _removeForwardSlash(self, aString) -> str:
        if len(aString) <= 2:
            return ""
        return aString[1:-1]

    def _validateRegexFilter(self, aRegexFilter: str):
        if aRegexFilter == "":
            raise ParsingError(f"regexFilter cannot be empty: {aRegexFilter}")
        # validating regexFilter with re.compile
        re.compile(aRegexFilter)
        return

    def _setUrlFilterInCondition(self, aCondition: Condition, aPattern: str):
        if self._isPatternRegexFilter(aPattern):
            return

        urlFilter: str = aPattern

        self._validateUrlFilter(urlFilter)
        aCondition.setUrlFilter(urlFilter)

    def _isPatternRegexFilter(self, aPattern: str):
        if aPattern.startswith('/') and aPattern.endswith('/'):
            return True
        else:
            return False

    def _validateUrlFilter(self, aUrlFilter: str):
        if aUrlFilter.startswith('||*'):
            raise ParsingError(f'urlFilter cannot start with ||*: {aUrlFilter}')
        if aUrlFilter == "":
            raise ParsingError(f'urlFilter cannot be empty: {aUrlFilter}')

        return

    def _extractOptionFrom(self, aUnformattedRule: str) -> str:
        option: str = aUnformattedRule.split('$', 1)[1]
        return option

    def _isOptionAList(self, aOption: str) -> bool:
        if ',' in aOption:
            return True
        return False

    def _splitOptions(self, aOption: str) -> List[str]:
        return aOption.split(',')

    def _setConditionUsingOptionList(self, aCondition: Condition, aOptionList: List[str]):
        for option in aOptionList:
            self._setDomainTypeInCondition(aCondition, option)
            self._setInitiatorDomainInCondition(aCondition, option)
            self._setResourceTypeInCondition(aCondition, option)
            self._activateUrlFilterCaseSensitiveInCondition(aCondition, option)

    def _setDomainTypeInCondition(self, aCondition: Condition, aOption: str):
        if not self.optionValidator.optionIsAValidDomainType(aOption):
            return

        if aCondition.isDomainTypeSet():
            raise ParsingError(f'double domain Type specified: {aOption}')

        domainType: str = self.optionValidator.transformDomainTypeValueToMv3CompatibleValue(aOption)

        aCondition.setDomainType(domainType)

    def _setInitiatorDomainInCondition(self, aCondition: Condition, aOption: str):
        if not self.optionValidator.optionIsAInitiatorDomain(aOption):
            return

        if aCondition.isInitiatorDomainSet():
            raise ParsingError(f'double domain found in rule: {aOption}')

        initiatorDomain: str = self._cleanInitiatorDomain(aOption)

        if self._isInitiatorDomainAList(initiatorDomain):
            initiatorDomainList: List[str] = self._splitInitiatorDomains(initiatorDomain)
            self._setListOfInitiatorDomainInCondition(initiatorDomainList, aCondition)
            return

        if self._isInitiatorDomainExcluded(initiatorDomain):
            initiatorDomain = self._removeNotSymbolFromString(initiatorDomain)
            aCondition.excludeInitiatorDomain(initiatorDomain)
        else:
            aCondition.includeInitiatorDomain(initiatorDomain)

    def _cleanInitiatorDomain(self, aInitiatorDomain: str) -> str:
        cleanInitiatorDomain: str = aInitiatorDomain.split('domain=', 1)[1]
        return cleanInitiatorDomain

    def _isInitiatorDomainAList(self, aInitiatorDomain: str) -> bool:
        if '|' in aInitiatorDomain:
            return True
        return False

    def _splitInitiatorDomains(self, aInitiatorDomain: str) -> list[str]:
        return aInitiatorDomain.split('|')

    def _setListOfInitiatorDomainInCondition(self, aInitiatorDomainList: List[str], aCondition: Condition):
        for initiatorDomain in aInitiatorDomainList:
            if self._isInitiatorDomainExcluded(initiatorDomain):
                initiatorDomain = self._removeNotSymbolFromString(initiatorDomain)
                aCondition.excludeInitiatorDomain(initiatorDomain)
            else:
                aCondition.includeInitiatorDomain(initiatorDomain)

    def _isInitiatorDomainExcluded(self, aInitiatorDomain: str) -> bool:
        if aInitiatorDomain.startswith('~'):
            return True

        return False

    def _setResourceTypeInCondition(self, aCondition: Condition, aOption: str):
        if not self.optionValidator.optionIsAValidResourceType(aOption):
            return

        resourceType: str = aOption

        if self._isResourceTypeExcluded(resourceType):
            resourceType = self._removeNotSymbolFromString(resourceType)
            resourceType = self.optionValidator.transformResourceTypeValueToMv3CompatibleValue(resourceType)

            if aCondition.doesResourceTypeExistsInResourceTypeList(resourceType):
                raise ParsingError(f'conflicting resource type and excluded resource type: {resourceType}')

            aCondition.excludeResourceType(resourceType)
        else:
            resourceType = self.optionValidator.transformResourceTypeValueToMv3CompatibleValue(resourceType)

            if aCondition.doesResourceTypeExistsInExcludedResourceTypeList(resourceType):
                raise ParsingError(f'conflicting resource type and excluded resource type: {resourceType}')

            aCondition.includeResourceType(resourceType)

    def _isResourceTypeExcluded(self, aResourceType: str) -> bool:
        if aResourceType.startswith('~'):
            return True

        return False

    def _removeNotSymbolFromString(self, aString: str) -> str:
        initiatorDomain = aString.split('~', 1)[1]

        return initiatorDomain

    def _activateUrlFilterCaseSensitiveInCondition(self, aCondition: Condition, aOption: str):
        optionValidator: UnFormattedRuleOptionValidator = UnFormattedRuleOptionValidator()
        if not optionValidator.optionIsAUrlFilterCaseSensitivitySetting(aOption):
            return

        caseSensitivitySetting: str = aOption

        if aCondition.isCaseSensitiveSet():
            raise ParsingError(f'conflicting resource type and excluded resource type: {caseSensitivitySetting}')

        aCondition.activateCaseSensitivity()

    def _isUnformattedRuleBlocking(self, aUnformattedRule: str) -> bool:
        if aUnformattedRule.startswith('@@'):
            return False
        return True

    def _instantiateAction(self, aType) -> Action:
        return Action(aType)

    def _instantiateMv3Rule(self, aId: int, aPriority: int, aAction: Action, aCondition: Condition) -> Mv3Rule:
        return Mv3Rule(aId, aPriority, aAction, aCondition)
