from typing import List

class Condition:
    def __init__(self):
        self.urlFilter: None | str = None
        self.regexFilter: None | str = None
        self.domainType: None | str = None
        self.initiatorDomain: None | List[str] = None
        self.excludedInitiatorDomain: None | List[str] = None
        self.resourceType: None | List[str] = None
        self.excludedResourceType: None | List[str] = None

    def setUrlFilter(self, aUrlFilter: str):
        self.urlFilter = aUrlFilter

    def setRegexFilter(self, aRegexFilter: str):
        newRegexFilter: str = self._removeForwardSlash(aRegexFilter)
        self.regexFilter = newRegexFilter

    def _removeForwardSlash(self, aString):
        if len(aString) <= 2:
            return ""
        return aString[1:-1]

    def setDomainType(self, aDomainType: str):
        if aDomainType.startswith('~'):
            self.domainType = 'firstParty'
        else:
            self.domainType = ' thirdParty'

    def setInitiatorDomain(self, aInitiatorDomainList: List[str]):
        for initiatorDomain in aInitiatorDomainList:
            if self._isInitiatorDomainExcluded(initiatorDomain):
                self._assignListToExcludedInitiatorDomain()
                initiatorDomainWithoutNotSymbol: str = self._removeNotSymbolFromString(initiatorDomain)
                self.excludedInitiatorDomain.append(initiatorDomainWithoutNotSymbol)
            else:
                self._assignListToInitiatorDomain()
                self.initiatorDomain.append(initiatorDomain)

    def _isInitiatorDomainExcluded(self, aInitiatorDomain: str) -> bool:
        if aInitiatorDomain.startswith('~'):
            return True
        return False

    def _assignListToExcludedInitiatorDomain(self):
        if self.excludedInitiatorDomain is None:
            self.excludedInitiatorDomain = []

    def _assignListToInitiatorDomain(self):
        if self.initiatorDomain is None:
            self.initiatorDomain = []

    def setResourceType(self, aResourceType: str):
        if self._isResourceTypeExclude(aResourceType):
            self._assignListToExcludedResourceType()
            resourceTypeWithoutNotSymbol: str = self._removeNotSymbolFromString(aResourceType)
            self.excludedResourceType.append(resourceTypeWithoutNotSymbol)
        else:
            self._assignListToResourceType()
            self.resourceType.append(aResourceType)

    def _isResourceTypeExclude(self, aResourceType: str) -> bool:
        if aResourceType.startswith('~'):
            return  True
        return False

    def _removeNotSymbolFromString(self, aString: str) -> str:
        return aString.split('~', 1)[1]

    def _assignListToExcludedResourceType(self):
        if self.excludedResourceType is None:
            self.excludedResourceType = []

    def _assignListToResourceType(self):
        if self.resourceType is None:
            self.resourceType = []

    def isDomainTypeNone(self):
        if self.domainType is None:
            return True
        return False

    def isInitiatorDomainSet(self):
        if not (self.initiatorDomain is None or self.excludedInitiatorDomain is None):
            return True
        return False
