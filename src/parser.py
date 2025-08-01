import re
from typing import List

from src.error import ParsingError
from src.fileImporter import FileImporter
from src.mv3Rule.mv3Rule import Mv3Rule
from src.mv3Rule.mv3RuleFactory import Mv3RuleFactory
from src.mv3RuleValidator import Mv3RuleValidator


class Parser:
    def parse(self, aFileName: str) -> List[Mv3Rule]:
        fileImporter: FileImporter = FileImporter()
        unformattedRuleList: List[str] = fileImporter.importUnformattedRuleFrom(aFileName)
        mv3RuleList: List[Mv3Rule] = self.__createMv3RuleList(unformattedRuleList)
        self.__validateMv3RuleList(mv3RuleList)

        return mv3RuleList

    def __createMv3RuleList(self, aUnFormattedRuleList: List[str]) -> List[Mv3Rule]:
        mv3RuleList: List[Mv3Rule] = []

        for i in range(len(aUnFormattedRuleList) - 1):
            try:
                mv3RuleFactory: Mv3RuleFactory = Mv3RuleFactory()
                mv3Rule: Mv3Rule = mv3RuleFactory.createMv3Rule(aUnFormattedRuleList[i], i)
                mv3RuleList.append(mv3Rule)
            except ParsingError:
                pass

        return mv3RuleList

    def __validateMv3RuleList(self, aMv3uleList: List[Mv3Rule]):
        for i in range(len(aMv3uleList) - 1, -1, -1):
            try:
                mv3RuleValidator: Mv3RuleValidator = Mv3RuleValidator()
                mv3RuleValidator.validate(aMv3uleList[i])
            except ParsingError or re.error:
                aMv3uleList.pop(i)
