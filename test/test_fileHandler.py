import json
import unittest
from typing import List, Dict, Any

from src.error import FilePathError
from src.fileHandler import FileHandler
from src.mv3Rule.mv3RuleFactory import Mv3RuleFactory
from src.mv3Rule.condition import Condition
from src.mv3Rule.action import Action
from src.mv3Rule.mv3Rule import Mv3Rule


class FileHandlerTestCase(unittest.TestCase):
    def test_should_import_only_networkFilteringRules(self):
        fileHandler: FileHandler = FileHandler()
        unFormattedRules: List[str] = fileHandler.readUnformattedRuleFrom(
            '/home/emmanuel/Desktop/urlPatternParser/test/rawRuleList/easylist.txt')

        for rule in unFormattedRules:
            # should not import empty string
            self.assertNotEqual(rule, '')
            # should not import comments
            self.assertNotEqual(rule[0], '!')
            # should not import content filters
            self.assertNotRegex(rule,
                                r'^(?:[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:\s*,\s*[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})*\s*)?(?:##|#[@$?]#)')

    def test_should_throw_an_error_if_inputFile_does_not_exist(self):
        fileHandler: FileHandler = FileHandler()

        self.assertRaises(FilePathError,
                          fileHandler.readUnformattedRuleFrom,
                          '/home/emmanuel/Desktop/urlPatternParser/rawRuleList/doesNotExist.txt')
        self.assertRaises(FilePathError,
                          fileHandler.readUnformattedRuleFrom,
                          '/home/emmanuel/Desktop/urlPatternParser/test/rawRuleList/')

    def test_should_throw_an_error_if_inputFile_extension_is_not_txt(self):
        fileHandler: FileHandler = FileHandler()

        self.assertRaises(FilePathError,
                          fileHandler.readUnformattedRuleFrom,
                          '/home/emmanuel/Desktop/urlPatternParser/rawRuleList/incorrectInputFileExtension')

    def test_should_generate_fullOutputFilePath(self):
        fileHandler: FileHandler = FileHandler()

        outputFolderPath: str = '/home/emmanuel/Desktop/urlPatternParser/test/processedMv3RuleList/'
        inputFilePath: str = '/home/emmanuel/Desktop/urlPatternParser/test/rawRuleList/testList.txt'

        expectedFullOutputFilePath: str = \
            '/home/emmanuel/Desktop/urlPatternParser/test/processedMv3RuleList/testList_processed.json'
        generatedFullOutputFilePath: str = fileHandler.generateOutPutFilePath(
            outputFolderPath,
            inputFilePath
        )

        self.assertEqual(generatedFullOutputFilePath, expectedFullOutputFilePath)

    def test_should_throw_error_if_outputFolderPath_is_a_filePath(self):
        fileHandler: FileHandler = FileHandler()

        outputFolderPath: str = '/home/emmanuel/Desktop/urlPatternParser/test/rawRuleList/testList.txt'
        inputFilePath: str = '/home/emmanuel/Desktop/urlPatternParser/test/rawRuleList/testList.txt'

        self.assertRaises(FilePathError, fileHandler.generateOutPutFilePath,
                          outputFolderPath, inputFilePath)

    def test_should_write_mv3Rule_to_file(self):
        outputFilePath: str = \
            '/home/emmanuel/Desktop/urlPatternParser/test/processedMv3RuleList/fileHandler_processed.json'

        self._write_mv3Rule_to_outputFile(outputFilePath)

        expectedRules: List[Dict[str, Any]]= self._expectedMv3Rule()
        generatedRules: List[Dict[str, Any]] = self._readRuleFromPath(outputFilePath)

        self.assertEqual(generatedRules, expectedRules)

    def _readRuleFromPath(self, aOutputFilePath) -> List[Dict[str, Any]]:
        retrievedRules: List[Dict[str, Any]]

        with open(aOutputFilePath, 'r') as file:
            retrievedRules = json.load(file)

        return retrievedRules

    def _write_mv3Rule_to_outputFile(self, aOutputFilePath):
        fileHandler: FileHandler = FileHandler()

        mv3RuleList: List[Mv3Rule] = self._createMv3List()

        fileHandler.writeMv3RuleJsonToOutputFile(aOutputFilePath, mv3RuleList)

    def _createMv3List(self) -> List[Mv3Rule]:
        mv3RuleList: List[Mv3Rule] = [self._blockingMv3Rule(), self._allowMv3Rule()]

        return mv3RuleList

    def _blockingMv3Rule(self):
        action: Action = Action('block')
        condition: Condition = Condition()
        mv3Rule: Mv3Rule

        condition.setUrlFilter('example.com')
        condition.includeResourceType('script')
        condition.excludeResourceType('xmlhttprequest')
        condition.setDomainType('thirdParty')

        mv3Rule = Mv3Rule(1, 1, action, condition)

        return mv3Rule

    def _allowMv3Rule(self):
        action: Action = Action('allow')
        condition: Condition = Condition()
        mv3Rule: Mv3Rule

        condition.setUrlFilter('example2.com')
        condition.includeResourceType('script')
        condition.excludeResourceType('xmlhttprequest')
        condition.setDomainType('thirdParty')

        mv3Rule = Mv3Rule(2, 2, action, condition)

        return mv3Rule

    def _expectedMv3Rule(self) -> List[Dict[str, Any]]:
        expectedMv3Rule = [
            {
                "id": 1,
                "priority": 1,
                "action": {
                    "type": "block"
                },
                "condition": {
                    "urlFilter": "example.com",
                    "domainType": "thirdParty",
                    "resourceType": [
                        "script"
                    ],
                    "excludedResourceType": [
                        "xmlhttprequest"
                    ]
                }
            },
            {
                "id": 2,
                "priority": 2,
                "action": {
                    "type": "allow"
                },
                "condition": {
                    "urlFilter": "example2.com",
                    "domainType": "thirdParty",
                    "resourceType": [
                        "script"
                    ],
                    "excludedResourceType": [
                        "xmlhttprequest"
                    ]
                }
            }
        ]

        return expectedMv3Rule



if __name__ == '__main__':
    unittest.main()
