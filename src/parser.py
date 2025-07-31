from typing import List
from src.result import Result
from src.mv3Rule.mv3Rule import Mv3Rule
from src.fileImporter import FileImporter
from src.mv3RuleValidator import Mv3RuleValidator
from src.mv3Rule.mv3RuleFactory import Mv3RuleFactory


class Parser:
    def __init__(self):
        self.result: Result = Result()

    def transform(self, aFileName: str):
        fileImporter: FileImporter = FileImporter()
        unformattedRuleList: List[str] = fileImporter.importUnformattedRuleFrom(aFileName)
        mv3RuleList: List[Mv3Rule] = []

        for i in range(len(unformattedRuleList) - 1):
            self.__createMv3RuleAndAppendToList(unformattedRuleList[i], mv3RuleList, i)

        for i in range(len(mv3RuleList) - 1):
            self.__validateMv3Rule(mv3RuleList[i])

        return self.result

    def __createMv3RuleAndAppendToList(self, aUnFormattedRule: str, aList: List[Mv3Rule], aId: int):
        try:
            mv3RuleFactory: Mv3RuleFactory = Mv3RuleFactory()
            mv3Rule: Mv3Rule = mv3RuleFactory.createMv3Rule(aUnFormattedRule, aId)
            aList.append(mv3Rule)

        except Exception():
            self.result.setInvalidUnFormattedRule(aUnFormattedRule)

    def __validateMv3Rule(self, aMv3ule: Mv3Rule):
        try:
            mv3RuleValidator: Mv3RuleValidator = Mv3RuleValidator()
            mv3RuleValidator.validate(aMv3ule)
            self.result.setValidMv3Rule(aMv3ule)
        except Exception():
            self.result.setInvalidMv3Rule(aMv3ule)
