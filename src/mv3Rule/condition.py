import re
from typing import List
from src.optionValidator import OptionValidator

class Condition:
    def __init__(self):
        self.urlFilter: None | str = None
        self.regexFilter: None | str = None
        self.domainType: None | str = None
        self.initiatorDomain: None | List[str] = None
        self.excludedInitiatorDomain: None | List[str] = None
        self.resourceType: None | List[str] = None
        self.excludedResourceType: None | List[str] = None
        self.optionValidator: OptionValidator = OptionValidator()

    def registerDomainType(self, aDomainType: str):
        self.__throwErrorIfDomainTypeExist()
        self.__throwErrorIfDomainTypeIsNotValid(aDomainType)
        if aDomainType == '~third-party':
            self.domainType = 'firstParty'
        elif aDomainType == 'third-party':
            self.domainType = 'thirdParty'
        else:
            raise Exception('incorrect domainType')

    def __throwErrorIfDomainTypeExist(self):
        if self.domainType is not None:
            raise Exception("conflict domainType")

    def __throwErrorIfDomainTypeIsNotValid(self, aDomainType: str):
        if self.domainTypeIsValid(aDomainType):
            return
        raise Exception("invalid domainType")

    def domainTypeIsValid(self, aDomainType: str):
        if self.optionValidator.valueIsAValidDomainType(aDomainType):
            return True
        return False

    def registerPattern(self, aPattern: str):
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

    def registerResourceType(self, aResourceType: str):
        self.__throwErrorIfResourceTypeIsNotValid(aResourceType)
        if aResourceType.startswith('~'):
            resourceTypeWithoutNotSymbol: str = self.__removeNotSymbolFromAString(aResourceType)
            self.__throwErrorIfResourceTypeIsConfigured(resourceTypeWithoutNotSymbol)
            self.__instantiateExcludedResourceTypeList()
            self.__appendResourceTypeToExcludedResourceTypeList(resourceTypeWithoutNotSymbol)
        else:
            self.__throwErrorIfResourceTypeIsConfigured(aResourceType)
            self.__instantiateResourceTypeList()
            self.__appendResourceTypeToResourceTypeList(aResourceType)

    def __throwErrorIfResourceTypeIsNotValid(self, aResourceType: str):
        if self.resourceTypeIsValid(aResourceType):
            return
        raise Exception("invalid domainType")

    def resourceTypeIsValid(self, aResourceType: str):
        if self.optionValidator.valueIsAValidDomainType(aResourceType):
            return True
        return False

    def __throwErrorIfResourceTypeIsConfigured(self, aResourceType: str):
        if aResourceType in self.resourceType or self.excludedResourceType:
            raise Exception("conflict resourceType")

    def __instantiateResourceTypeList(self):
        if self.resourceType is None:
            self.resourceType = []

    def __instantiateExcludedResourceTypeList(self):
        if self.excludedResourceType is None:
            self.excludedResourceType = []

    def __appendResourceTypeToExcludedResourceTypeList(self, aResourceType: str):
        self.excludedResourceType.append(aResourceType)

    def __appendResourceTypeToResourceTypeList(self, aResourceType: str):
        self.resourceType.append(aResourceType)

    def registerInitiatorDomain(self, aDomainName: str):
        self.__throwErrorIfIncludedOrExcludedInitiatorDomainIsSet()
        if self.__domainIsaList(aDomainName):
            domainNameList: List[str] = self.__splitDomain(aDomainName)
            self.__throwErrorIfConflictingDomainNameExistsIn(domainNameList)
            self.__registerAllInitiatorDomainInList(domainNameList)
        else:
            if aDomainName.startswith('~'):
                self.__instantiateExcludedInitiatorDomain()
                domainWithoutNotSymbol = self.__removeNotSymbolFromAString(aDomainName)
                self.__appendInitiatorDomainToExcludedInitiatorDomain(domainWithoutNotSymbol)
            else:
                self.__instantiateInitiatorDomain()
                self.__appendInitiatorDomainToInitiatorDomain(aDomainName)

    def __throwErrorIfIncludedOrExcludedInitiatorDomainIsSet(self):
        if self.initiatorDomain is not None or self.excludedInitiatorDomain is not None:
            raise Exception("duplicate domain=")

    def __domainIsaList(self, aDomain: str):
        if '|' in aDomain:
            return True
        else:
            return False

    def __splitDomain(self, aDomain: str) -> List[str]:
        listOfDomain: List[str] = aDomain.split('|')
        return listOfDomain

    def __throwErrorIfConflictingDomainNameExistsIn(self, aDomainNameList: List[str]):
        newDomainList: List[str] = self.__removeNotSymbolFromListOfString(aDomainNameList)
        for domainName in newDomainList:
            if newDomainList.count(domainName)> 1:
                raise Exception("conflict domain name")

    def __removeNotSymbolFromListOfString(self, aStringList: List[str]) -> List[str]:
        stringList: List[str] = aStringList.copy()
        for i in range(len(stringList) - 1):
            if stringList[i].startswith('~'):
                stringList[i] = stringList[i].lstrip('~')
        return stringList

    def __registerAllInitiatorDomainInList(self, aDomainNameList: List[str]):
        for domainName in aDomainNameList:
            if domainName.startswith('~'):
                self.__instantiateExcludedInitiatorDomain()
                domainWithoutNotSymbol = self.__removeNotSymbolFromAString(domainName)
                self.__appendInitiatorDomainToExcludedInitiatorDomain(domainWithoutNotSymbol)
            else:
                self.__instantiateInitiatorDomain()
                self.__appendInitiatorDomainToInitiatorDomain(domainName)

    def __appendInitiatorDomainToExcludedInitiatorDomain(self, aDomainName):
        self.excludedInitiatorDomain.append(aDomainName)

    def __appendInitiatorDomainToInitiatorDomain(self, aDomainName):
        self.initiatorDomain.append(aDomainName)

    def __removeNotSymbolFromAString(self, string: str) -> str:
        return string.lstrip('~')

    def __instantiateExcludedInitiatorDomain(self):
        if self.excludedInitiatorDomain is None:
            self.excludedInitiatorDomain = []

    def __instantiateInitiatorDomain(self):
        if self.initiatorDomain is None:
            self.initiatorDomain = []