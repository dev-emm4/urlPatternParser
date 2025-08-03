import unittest
from typing import List

from src.mv3Rule.mv3Rule import Mv3Rule
from src.parser import Parser

class ParserTestCase(unittest.TestCase):
    def test_should_create_mv3rule_from_valid_rule(self):
        parser: Parser = Parser()
        mv3RuleList: List[Mv3Rule] = parser.parse(
            '/home/emmanuel/Desktop/urlPatternParser/test/rawRuleList/testList.txt')

        self.assertEqual(len(mv3RuleList), 2)
        self.assertEqual(mv3RuleList[0].condition.urlFilter, '/parser.com')
        self.assertEqual(mv3RuleList[1].condition.urlFilter, '/parser.net/*')


if __name__ == '__main__':
    unittest.main()
