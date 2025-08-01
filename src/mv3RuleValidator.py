import re

from src.error import ParsingError
from src.mv3Rule.mv3Rule import Mv3Rule


class Mv3RuleValidator:
    def validate(self, aMv3Rule: Mv3Rule):
        self._throwErrorIfRegexFilterIsInvalid(aMv3Rule)
        self._throwErrorIfUrlFilterIsInvalid(aMv3Rule)
        self._throwErrorIfResourceTypeAndExcludedResourceTypeContainsConflictingValues(aMv3Rule)
        return

    def _throwErrorIfRegexFilterIsInvalid(self, aMv3Rule: Mv3Rule):
        if aMv3Rule.condition.regexFilter is None:
            return
        if aMv3Rule.condition.regexFilter == "":
            raise ParsingError("regexFilter cannot be empty")

        #validating regexFilter with re.compile
        re.compile(aMv3Rule.condition.regexFilter)
        return

    def _throwErrorIfUrlFilterIsInvalid(self, aMv3Rule: Mv3Rule):
        if aMv3Rule.condition.urlFilter is None:
            return
        if aMv3Rule.condition.urlFilter.startswith('||*'):
            raise ParsingError('urlFilter cannot start with ||*')
        if aMv3Rule.condition.urlFilter == "":
            raise ParsingError('urlFilter cannot be empty')

        return

    def _throwErrorIfResourceTypeAndExcludedResourceTypeContainsConflictingValues(self, aMv3Rule: Mv3Rule):
        if aMv3Rule.condition.resourceType is None or aMv3Rule.condition.excludedResourceType is None:
            return

        for resourceType in aMv3Rule.condition.resourceType:
            if resourceType in aMv3Rule.condition.excludedResourceType:
                raise ParsingError(f'conflicting resource type and excluded resource type: {resourceType}')
        return
