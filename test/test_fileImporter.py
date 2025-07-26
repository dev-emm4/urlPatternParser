import re
import unittest
from typing import List
from src.fileImporter import FileImporter

class FieImporterTestCase(unittest.TestCase):
    def test_should_import_only_networkFilteringRules(self):
        importer = FileImporter()
        unFormattedRules: List[str] = importer.importUnformattedRuleFrom('easylist.txt')
        for rule in unFormattedRules:
            # should not import empty string
            self.assertNotEqual(rule, '')
            # should not import comments
            self.assertNotEqual(rule[0], '!')
            # should not import content filters
            self.assertNotRegex(rule, r'^(?:[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:\s*,\s*[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})*\s*)?(?:##|#[@$?]#)')


if __name__ == '__main__':
    unittest.main()
