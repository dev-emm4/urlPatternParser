import re
from typing import List

from error import ParsingError
from fileHandler import FileHandler
from mv3Rule.mv3Rule import Mv3Rule
from mv3Rule.mv3RuleFactory import Mv3RuleFactory


class Parser:
    def convert(self, aInputFilePath: str, aOutputFolderPath: str, aMaxLength: int):
        fileHandler: FileHandler = FileHandler()

        unformattedRuleList: List[str] = fileHandler.readUnformattedRuleFrom(aInputFilePath)
        mv3RuleList: List[Mv3Rule] = self.__createMv3RuleList(unformattedRuleList, aMaxLength)
        fullOutputFilePath: str = fileHandler.generateOutPutFilePath(aOutputFolderPath, aInputFilePath)

        fileHandler.writeMv3RuleJsonToOutputFile(fullOutputFilePath, mv3RuleList)

    def __createMv3RuleList(self, aUnFormattedRuleList: List[str], aMaxLength: int) -> List[Mv3Rule]:
        mv3RuleFactory: Mv3RuleFactory = Mv3RuleFactory()
        mv3RuleList: List[Mv3Rule] = []
        maxLength: int = aMaxLength
        index: int = 0

        while index < maxLength and  index < len(aUnFormattedRuleList):
            try:
                mv3Rule: Mv3Rule = mv3RuleFactory.createMv3Rule(aUnFormattedRuleList[index], index)
                mv3RuleList.append(mv3Rule)
            except ParsingError as e:
                print(f"Parsing error at index {index}: {e}")
                pass
            except re.error as e:
                print(f"Parsing error at index {index}: {e}")
                pass
            finally:
                index = index + 1

        return mv3RuleList
