import re
from typing import List
from error import ParsingError


class UnFormattedRuleOptionValidator:
    def __init__(self):
        self._resourceTypeValues: List[str] = ['script', 'image', 'stylesheet', 'object', 'xmlhttprequest',
                                              'subdocument', 'ping', 'websocket', 'document',
                                              '~script', '~image', '~stylesheet', '~object', '~xmlhttprequest',
                                              '~subdocument', '~ping', '~websocket', '~document',
                                               '~other', 'popup', 'font', 'media', 'other']
        self._domainTypeValues: List[str] = ['third-party', '~third-party']
        self._caseSensitivitySetting: str = 'match-case'

    def transformDomainTypeValueToMv3CompatibleValue(self, aDomainType: str) -> str:
        if aDomainType == 'third-party':
            return 'thirdParty'
        elif aDomainType == '~third-party':
            return 'firstParty'

        raise ParsingError(f'expected domainType value but got: {aDomainType}')

    def transformResourceTypeValueToMv3CompatibleValue(self, aResourceType: str) -> str:
        if aResourceType == 'document':
            return 'main_frame'
        elif aResourceType == 'subdocument':
            return 'sub_frame'
        elif aResourceType in self._resourceTypeValues:
            return aResourceType

        raise ParsingError(f'expected resourceType value but got: {aResourceType}')


    def optionIsAValidResourceType(self, aOption: str) -> bool:
        if aOption in self._resourceTypeValues:
            return True

        return False

    def optionIsAValidDomainType(self, aOption: str) -> bool:
        if aOption in self._domainTypeValues:
            return True

        return False

    def optionIsAInitiatorDomain(self, aOption: str) -> bool:
        pattern: str = r'^domain='
        if re.match(pattern, aOption):
            return True

        return False

    def optionIsAUrlFilterCaseSensitivitySetting(self, aOption: str) -> bool:
        if aOption == self._caseSensitivitySetting:
            return True

        return False
