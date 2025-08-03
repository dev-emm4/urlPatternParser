import json
import unittest
from typing import List, Dict, Any

from src.parser import Parser


class ParserTestCase(unittest.TestCase):
    def test_should_generate_mv3rule_from_valid_rule(self):
        parser: Parser = Parser()

        inputFilePath: str = '/home/emmanuel/Desktop/urlPatternParser/test/rawRuleList/testList.txt'
        outputFolderPath: str = '/home/emmanuel/Desktop/urlPatternParser/test/processedMv3RuleList/'

        parser.covert(inputFilePath, outputFolderPath)

        generatedRules: List[Dict[str, Any]] = self._readRuleFromPath(outputFolderPath + 'testList_processed.json')
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
                    "urlFilter": "/parser.com",
                    "resourceType": [
                        "stylesheet"
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
                    "urlFilter": "/parser.net/*",
                    "excludedInitiatorDomain": [
                        "kamaz-service.kz",
                        "theatreticketsdirect.co.uk"
                    ],
                    "resourceType": [
                        "image"
                    ]
                }
            }]
        return expectedRules


if __name__ == '__main__':
    unittest.main()
