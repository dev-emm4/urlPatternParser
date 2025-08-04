from typing import List

class Locations:
    def __init__(self):
        self._inputFilePaths: List[str] =  [
            '/home/emmanuel/Desktop/urlPatternParser/test/rawRuleList/easylist.txt',
            '/home/emmanuel/Desktop/urlPatternParser/test/rawRuleList/easyprivacy.txt',
            '/home/emmanuel/Desktop/urlPatternParser/test/rawRuleList/testList.txt',
            '/home/emmanuel/Desktop/urlPatternParser/test/rawRuleList/incorrectInputFileExtension']
        self._outputFolder: str = '/home/emmanuel/Desktop/urlPatternParser/test/processedMv3RuleList/'

    def getInputFilePath(self, index: int) -> str:
        return self._inputFilePaths[index]

    def getInputFilePathFor(self, fileName) -> str:
        for inputFilePath in self._inputFilePaths:
            if fileName in inputFilePath:
                return inputFilePath

        raise Exception('file path not defined')

    def getOutputFolderPath(self) -> str:
        return self._outputFolder
