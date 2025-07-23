import re
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

    def setDomainType(self, aDomainType: str):
        self.__throwErrorIfDomainTypeExist()
        self.domainType = aDomainType

    def __throwErrorIfDomainTypeExist(self):
        if self.domainType is not None:
            raise Exception("conflict domainType")

    def setPattern(self, aPattern: str):
        self.__throwErrorIfPatternExist()
        if self.__patternIsRegex(aPattern):
            self.regexFilter = aPattern
        else:
            self.urlFilter = aPattern

    def __throwErrorIfPatternExist(self):
        if self.regexFilter is not None or self.urlFilter is not None:
            raise Exception("conflict pattern")

    def __patternIsRegex(self, aPattern: str):
        return bool(re.match(r'^/.*/$', aPattern))

    def setResource(self, aResource: str):
        if aResource.startswith('~'):
            resourceWithoutNotSymbol: str = self.__removeNotSymbolFromString(aResource)
            self.__throwErrorIfResourceExist(resourceWithoutNotSymbol)
            self.__instantiateResourceType()
            self.resourceType.append(resourceWithoutNotSymbol)
        else:
            self.__throwErrorIfResourceExist(aResource)
            self.__instantiateExcludedResourceType()
            self.excludedResourceType.append(aResource)

    def __throwErrorIfResourceExist(self, aResource: str):
        if aResource in self.resourceType or self.excludedResourceType:
            raise Exception("conflict resourceType")

    def __instantiateResourceType(self):
        if self.resourceType is None:
            self.resourceType = []

    def __instantiateExcludedResourceType(self):
        if self.excludedResourceType is None:
            self.excludedResourceType = []

    def setDomain(self, aDomain: str):
        self.__throwErrorIfDomainExist()
        if self.__domainIsaList(aDomain):
            listOfDomain: List[str] = self.__getListOfDomain(aDomain)
            self.__setInitiatorOrExcludedInitiatorDomainFromList(listOfDomain)
        else:
            self.__setInitiatorOrExcludedInitiatorDomain(aDomain)

    def __throwErrorIfDomainExist(self):
        if self.initiatorDomain is not None or self.excludedInitiatorDomain is not None:
            raise Exception("conflict domain")

    def __domainIsaList(self, domain: str):
        if '|' in domain:
            return True
        else:
            return False

    def __getListOfDomain(self, domain: str) -> List[str]:
        listOfDomain: List[str] = domain.split('|')
        return listOfDomain

    def __setInitiatorOrExcludedInitiatorDomainFromList(self, aListOfDomain: List[str]):
        for domain in aListOfDomain:
            if domain.startswith('~'):
                self.__instantiateExcludedInitiatorDomain()
                domainWithoutNotSymbol = self.__removeNotSymbolFromString(domain)
                self.excludedInitiatorDomain.append(domainWithoutNotSymbol)
            else:
                self.__instantiateInitiatorDomain()
                self.initiatorDomain.append(domain)

    def __removeNotSymbolFromString(self, string: str) -> str:
        return string.lstrip('~')

    def __setInitiatorOrExcludedInitiatorDomain(self, domain: str):
        if domain.startswith('~'):
            self.__instantiateExcludedInitiatorDomain()
            domainWithoutNotSymbol = self.__removeNotSymbolFromString(domain)
            self.excludedInitiatorDomain.append(domainWithoutNotSymbol)
        else:
            self.__instantiateInitiatorDomain()
            self.initiatorDomain.append(domain)

    def __instantiateExcludedInitiatorDomain(self):
        if self.excludedInitiatorDomain is None:
            self.excludedInitiatorDomain = []

    def __instantiateInitiatorDomain(self):
        if self.initiatorDomain is None:
            self.initiatorDomain = []