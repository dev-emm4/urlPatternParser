from typing import List
from mv3Rule import Mv3Rule

class Parser:
    def parseFromFile(self, location: str) -> List[Mv3Rule]:
        try:
            # rules in string format
            stringRules: List[str] = self._importFileFrom(location)
            self._refineAllStringRule(stringRules)
        except Exception as e:
            print('an error has occurred: ', e)
            raise e

    def _importFileFrom(self, location: str) -> List[str]:
        try:
            # '././rawRuleList/' is an absolute path
            with open('././rawRuleList/' + location, 'r') as file:
                stringRules: List[str] = file.read().splitlines()
            return stringRules
        except Exception as e:
            raise e

    def _refineAllStringRule(self, stringRules: List[str]):
        self._throwErrorIfStringRulesIsEmpty(stringRules)

        self._removeTrailingSpacesFromStringRules(stringRules)

        self._removeStringRuleOfSize0(stringRules)
        self._throwErrorIfStringRulesIsEmpty(stringRules)

        self._removeCommentFromStringRules(stringRules)
        self._throwErrorIfStringRulesIsEmpty(stringRules)

    def _removeTrailingSpacesFromStringRules(self, stringRules: List[str]):
        for stringRule in stringRules:
            stringRule.strip()

    def _removeStringRuleOfSize0(self, stringRules: List[str]):
        # looping backwards "range - 1, -1, -1"
        for i in range(len(stringRules) - 1, -1, -1):
            if len(stringRules[i]) < 1:
                stringRules.pop(i)

    def _removeCommentFromStringRules(self, stringRules: List[str]):
        # looping backwards "range - 1, -1, -1"
        for i in range(len(stringRules) - 1, -1, -1):
            if stringRules[i][0] == '!':
                stringRules.pop(i)

    def _throwErrorIfStringRulesIsEmpty(self, stringRules: List[str]):
        if len(stringRules) < 1:
            raise "list is empty"
        else:
            return
