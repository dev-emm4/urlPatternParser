import json
import unittest
from typing import List, Dict, Any

from locations import Locations
from src.parser import Parser


class ParserTestCase(unittest.TestCase):
    def setUp(self):
        self.locations = Locations()
        self.parser: Parser = Parser()

    def test_should_generate_specified_length_of_rules(self):
        inputFilePath: str = self.locations.getInputFilePathFor('easylist.txt')
        outputFolderPath: str = self.locations.getOutputFolderPath()
        maxLength: int = 1000

        self.parser.convert(inputFilePath, outputFolderPath, maxLength)

        generatedRules: List[Dict[str, Any]] = self._readRuleFromPath(outputFolderPath + 'easylist_processed.json')

        self.assertEqual(len(generatedRules), maxLength)

    def test_should_generate_mv3rule_from_valid_rule(self):
        inputFilePath: str = self.locations.getInputFilePathFor('parserInputRule.txt')
        outputFolderPath: str = self.locations.getOutputFolderPath()

        self.parser.convert(inputFilePath, outputFolderPath)

        generatedRules: List[Dict[str, Any]] = self._readRuleFromPath(outputFolderPath + 'parserInputRule_processed.json')
        expectedRules: List[Dict[str, Any]] = self._expectedRules()

        self.assertEqual(generatedRules, expectedRules)


    def _readRuleFromPath(self, aOutputFilePath) -> List[Dict[str, Any]]:
        retrievedRules: List[Dict[str, Any]]

        with open(aOutputFilePath, 'r') as file:
            retrievedRules = json.load(file)

        return retrievedRules

    def _expectedRules(self) -> List[Dict[str, Any]]:
        expectedRules: List[Dict[str, Any]] = [
            {
                "id": 0,
                "priority": 1,
                "action": {
                    "type": "block"
                },
                "condition": {
                    "urlFilter": "/example.com",
                    "resourceType": [
                        "stylesheet",
                        "script",
                        "image"
                    ]
                }
            },
            {
                "id": 1,
                "priority": 1,
                "action": {
                    "type": "block"
                },
                "condition": {
                    "urlFilter": "/example.com/*",
                    "excludedInitiatorDomain": [
                        "second.example.com",
                        "third.example.com"
                    ],
                    "resourceType": [
                        "image"
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
                    "urlFilter": "/example.com",
                    "resourceType": [
                        "stylesheet",
                        "script",
                        "image"
                    ]
                }
            },
            {
                "id": 3,
                "priority": 1,
                "action": {
                    "type": "block"
                },
                "condition": {
                    "urlFilter": "example.com"
                }
            }
        ]
        return expectedRules


if __name__ == '__main__':
    unittest.main()
