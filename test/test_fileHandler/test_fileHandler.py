import json
import unittest
from typing import List, Dict, Any

from error import FilePathError
from fileHandler import FileHandler
from locations import Locations
from mv3Rule.action import Action
from mv3Rule.condition import Condition
from mv3Rule.mv3Rule import Mv3Rule


class FileHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.fileHandler: FileHandler = FileHandler()
        self.locations: Locations = Locations()

    def test_should_import_only_networkFilteringRules(self):
        unFormattedRules: List[str] = self.fileHandler.readUnformattedRuleFrom(
            self.locations.getInputFilePathFor('fileHandlerInputRules.txt'))

        for rule in unFormattedRules:
            # should not import empty string
            self.assertNotEqual(rule, '')
            # should not import comments
            self.assertNotEqual(rule[0], '!')
            # should not import content filters
            self.assertNotIn('##', rule)
            self.assertNotIn('#@#', rule)
            self.assertNotIn('#$#', rule)
            self.assertNotIn('#?#', rule)

    def test_should_throw_an_error_if_inputFile_does_not_exist(self):
        self.assertRaises(FilePathError,
                          self.fileHandler.readUnformattedRuleFrom,
                          self.locations.getOutputFolderPath() + 'doesNotExist.txt')
        self.assertRaises(FilePathError,
                          self.fileHandler.readUnformattedRuleFrom,
                          self.locations.getOutputFolderPath())

    def test_should_throw_an_error_if_inputFile_extension_is_not_txt(self):
        self.assertRaises(FilePathError,
                          self.fileHandler.readUnformattedRuleFrom,
                          self.locations.getInputFilePathFor('incorrectInputFileExtension'))

    def test_should_generate_fullOutputFilePath(self):
        expectedFullOutputFilePath: str = \
            '/home/emmanuel/Desktop/urlPatternParser/test/processedMv3RuleList/fileHandlerInputRules_processed.json'
        generatedFullOutputFilePath: str = self.fileHandler.createOutPutFile(
            self.locations.getOutputFolderPath(),
            self.locations.getInputFilePathFor('fileHandlerInputRules.txt')
        )

        self.assertEqual(generatedFullOutputFilePath, expectedFullOutputFilePath)

    def test_should_throw_error_if_outputFolderPath_is_a_filePath(self):
        self.assertRaises(FilePathError, self.fileHandler.createOutPutFile,
                          self.locations.getInputFilePathFor('easylist.txt'),
                          self.locations.getInputFilePathFor('easylist.txt'))

    def test_should_write_mv3Rule_to_file(self):
        outputFilePath: str = \
            self.locations.getOutputFolderPath() + 'fileHandler_processed.json'

        self._write_mv3Rule_to_outputFile(outputFilePath)

        generatedRules: List[Dict[str, Any]] = self._readGeneratedRulesFromPath(outputFilePath)
        expectedGeneratedRules: List[Dict[str, Any]] = self._expectedGeneratedRule()

        self.assertEqual(generatedRules, expectedGeneratedRules)

    def _write_mv3Rule_to_outputFile(self, aOutputFilePath):
        mv3RuleList: List[Mv3Rule] = self._createMv3List()

        self.fileHandler.writeMv3RuleToOutputFile(aOutputFilePath, mv3RuleList)

    def _createMv3List(self) -> List[Mv3Rule]:
        mv3RuleList: List[Mv3Rule] = [self._blockingMv3Rule(), self._allowMv3Rule()]

        return mv3RuleList

    def _readGeneratedRulesFromPath(self, aOutputFilePath) -> List[Dict[str, Any]]:
        retrievedRules: List[Dict[str, Any]]

        with open(aOutputFilePath, 'r') as file:
            retrievedRules = json.load(file)

        return retrievedRules

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

    def _expectedGeneratedRule(self) -> List[Dict[str, Any]]:
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
                    "resourceTypes": [
                        "script"
                    ],
                    "excludedResourceTypes": [
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
                    "resourceTypes": [
                        "script"
                    ],
                    "excludedResourceTypes": [
                        "xmlhttprequest"
                    ]
                }
            }
        ]

        return expectedMv3Rule


if __name__ == '__main__':
    unittest.main()
