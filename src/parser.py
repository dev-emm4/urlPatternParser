import re
from typing import List

from src.error import ParsingError
from src.fileHandler import FileHandler
from src.mv3Rule.mv3Rule import Mv3Rule
from src.mv3Rule.mv3RuleFactory import Mv3RuleFactory


class Parser:
    def parse(self, aInputFilePath: str) -> List[Mv3Rule]:
        fileHandler: FileHandler = FileHandler()
        unformattedRuleList: List[str] = fileHandler.readUnformattedRuleFrom(aInputFilePath)
        mv3RuleList: List[Mv3Rule] = self.__createMv3RuleList(unformattedRuleList)

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
