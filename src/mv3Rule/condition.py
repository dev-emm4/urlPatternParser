from typing import List

class Condition:
    def __init__(self):
        self.urlFilter: None | str = None
        self.regexFilter: None | str = None
        self.domainType: None | str = None
        self.initiatorDomain: None | List[str] = None
        self.excludedInitiatorDomain: None | List[str] = None
        self.resourceTypes: None | List[str] = None
        self.excludedResourceTypes: None | List[str] = None
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
        self.resourceTypes.append(aResourceType)

    def _assignListToResourceType(self):
        if self.resourceTypes is None:
            self.resourceTypes = []

    def excludeResourceType(self, aResourceType: str):
        self._assignListToExcludedResourceType()
        self.excludedResourceTypes.append(aResourceType)

    def _assignListToExcludedResourceType(self):
        if self.excludedResourceTypes is None:
            self.excludedResourceTypes = []

    def activateCaseSensitivity(self):
        self.isUrlFilterCaseSensitive = True

    def doesResourceTypeExistsInExcludedResourceTypeList(self, aResourceType: str) -> bool:
        if self.excludedResourceTypes is None:
            return False

        for resourceType in self.excludedResourceTypes:
            if aResourceType == resourceType:
                return True

        return  False

    def doesResourceTypeExistsInResourceTypeList(self, aResourceType: str) -> bool:
        if self.resourceTypes is None:
            return False

        for resourceType in self.resourceTypes:
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
