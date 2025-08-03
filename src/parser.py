from typing import List

from error import ParsingError
from fileHandler import FileHandler
from mv3Rule.mv3Rule import Mv3Rule
from mv3Rule.mv3RuleFactory import Mv3RuleFactory


class Parser:
    def covert(self, aInputFilePath: str, aOutputFolderPath: str):
        fileHandler: FileHandler = FileHandler()

        unformattedRuleList: List[str] = fileHandler.readUnformattedRuleFrom(aInputFilePath)
        mv3RuleList: List[Mv3Rule] = self.__createMv3RuleList(unformattedRuleList)
        fullOutputFilePath: str = fileHandler.generateOutPutFilePath(aOutputFolderPath, aInputFilePath)

        fileHandler.writeMv3RuleJsonToOutputFile(fullOutputFilePath, mv3RuleList)

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


