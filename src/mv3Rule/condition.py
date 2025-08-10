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
        self.isUrlFilterCaseSensitive : None | bool = None

    def setUrlFilter(self, aUrlFilter: str):
        self.urlFilter = aUrlFilter

    def setRegexFilter(self, aRegexFilter: str):
        self.regexFilter = aRegexFilter

    def setDomainType(self, aDomainType: str):
        self.domainType = aDomainType

    def includeInitiatorDomain(self, aInitiatorDomain: str):
        self._assignListToInitiatorDomain()
        self.initiatorDomain.append(aInitiatorDomain)

    def _assignListToInitiatorDomain(self):
        if self.initiatorDomain is None:
            self.initiatorDomain = []

    def excludeInitiatorDomain(self, aInitiatorDomain: str):
        self._assignListToExcludedInitiatorDomain()
        self.excludedInitiatorDomain.append(aInitiatorDomain)

    def _assignListToExcludedInitiatorDomain(self):
        if self.excludedInitiatorDomain is None:
            self.excludedInitiatorDomain = []

    def includeResourceType(self, aResourceType: str):
        self._assignListToResourceType()
        self.resourceType.append(aResourceType)

    def _assignListToResourceType(self):
        if self.resourceType is None:
            self.resourceType = []

    def excludeResourceType(self, aResourceType: str):
        self._assignListToExcludedResourceType()
        self.excludedResourceType.append(aResourceType)

    def _assignListToExcludedResourceType(self):
        if self.excludedResourceType is None:
            self.excludedResourceType = []

    def activateCaseSensitivity(self):
        self.isUrlFilterCaseSensitive = True

    def doesResourceTypeExistsInExcludedResourceTypeList(self, aResourceType: str) -> bool:
        if self.excludedResourceType is None:
            return False

        for resourceType in self.excludedResourceType:
            if aResourceType == resourceType:
                return True

        return  False

    def doesResourceTypeExistsInResourceTypeList(self, aResourceType: str) -> bool:
        if self.resourceType is None:
            return False

        for resourceType in self.resourceType:
            if aResourceType == resourceType:
                return True

        return False

    def isDomainTypeSet(self):
        if self.domainType is not None:
            return True

        return False

    def isInitiatorDomainSet(self):
        if self.initiatorDomain is not None or self.excludedInitiatorDomain is not None:
            return True

        return False

    def isCaseSensitiveSet(self) -> bool:
        if self.isUrlFilterCaseSensitive is not None:
            return True
        return False

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}
