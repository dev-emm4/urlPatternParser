from typing import List


class Locations:
    def __init__(self):
        self._inputFilePaths: List[str] = [
            '/home/emmanuel/Desktop/urlPatternParser/test/generalInputRules/easylist.txt',
            '/home/emmanuel/Desktop/urlPatternParser/test/generalInputRules/easyprivacy.txt',
            '/home/emmanuel/Desktop/urlPatternParser/test/generalInputRules/incorrectInputFileExtension',
            '/home/emmanuel/Desktop/urlPatternParser/test/test_fileHandler/fileHandlerInputRules.txt',
            '/home/emmanuel/Desktop/urlPatternParser/test/test_parser/parserInputRule.txt']
        self._outputFolder: str = '/home/emmanuel/Desktop/urlPatternParser/test/processedMv3RuleList/'

    def getInputFilePathFor(self, fileName) -> str:
        for inputFilePath in self._inputFilePaths:
            if fileName in inputFilePath:
                return inputFilePath

        raise Exception('file path not defined')

    def getOutputFolderPath(self) -> str:
        return self._outputFolder
