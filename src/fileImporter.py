import re
from typing import List


class FileImporter:
    def importUnformattedRuleFrom(self, aFileName: str) -> List[str]:
        try:
            # rules in string format
            stringList: List[str]
            # '././rawRuleList/' is an absolute path
            with open('../rawRuleList/' + aFileName, 'r') as file:
                stringList: List[str] = file.read().splitlines()

            unformattedRules: List[str] = self._getUnformattedFilteringRulesFrom(stringList)
            return unformattedRules
        except Exception as e:
            print('an error has occurred: ', e)
            raise e

    def _getUnformattedFilteringRulesFrom(self, aStringList: List[str]) -> List[str]:
        unformattedRules: List[str] = []
        for string in aStringList:
            stringWithoutSpace: str = self._removeSpacesFromString(string)
            if self._isStringANetworkFilteringRule(stringWithoutSpace):
                unformattedRules.append(stringWithoutSpace)

        return unformattedRules

    def _removeSpacesFromString(self, aString: str) -> str:
        return re.sub(r'\s+', '', aString)

    def _isStringANetworkFilteringRule(self, aString: str) -> bool:
        if aString == "":
            return False
        elif aString.startswith('!'):
            return False
        elif re.match(r'^(?:[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:\s*,\s*[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})*\s*)?(?:##|#[@$?]#)',
                      aString):
            return False
        else:
            return True
