import re
import unittest

from error import ParsingError
from mv3Rule.mv3Rule import Mv3Rule
from mv3Rule.mv3RuleFactory import Mv3RuleFactory


class Mv3RuleFactoryTestCase(unittest.TestCase):
    def setUp(self):
        self.mv3RuleFactory: Mv3RuleFactory = Mv3RuleFactory()

    def test_should_create_blocking_Mv3Rule(self):
        unFormattedRule: str = \
            '/exoclick.$~script,~xmlhttprequest,document,domain=~exoclick.bamboohr.co.uk|~exoclick.kayako.com'
        mv3Rule: Mv3Rule = self.mv3RuleFactory.createMv3Rule(unFormattedRule, 1)

        self.assertEqual(mv3Rule.id, 1)
        self.assertEqual(mv3Rule.priority, 1)
        self.assertEqual(mv3Rule.condition.urlFilter, '/exoclick.')
        self.assertEqual(mv3Rule.condition.domainType, None)
        self.assertEqual(mv3Rule.action.type, 'block')
        self.assertIn('main_frame', mv3Rule.condition.resourceTypes)
        self.assertIn('exoclick.bamboohr.co.uk', mv3Rule.condition.excludedInitiatorDomain)
        self.assertIn('exoclick.kayako.com', mv3Rule.condition.excludedInitiatorDomain)
        self.assertIn('xmlhttprequest', mv3Rule.condition.excludedResourceTypes)
        self.assertIn('script', mv3Rule.condition.excludedResourceTypes)
        self.assertIsNone(mv3Rule.condition.isUrlFilterCaseSensitive)

    def test_should_create_allowing_Mv3Rule(self):
        unFormattedRule: str = \
            '@@/exoclick/$script,~xmlhttprequest,~subdocument,domain=exoclick.bamboohr.co.uk|~exoclick.kayako.com,~third-party,match-case'
        mv3Rule: Mv3Rule = self.mv3RuleFactory.createMv3Rule(unFormattedRule, 1)

        self.assertEqual(mv3Rule.id, 1)
        self.assertEqual(mv3Rule.priority, 2)
        self.assertEqual(mv3Rule.condition.regexFilter, 'exoclick')
        self.assertEqual(mv3Rule.condition.domainType, 'firstParty')
        self.assertEqual(mv3Rule.action.type, 'allow')
        self.assertIn('exoclick.bamboohr.co.uk', mv3Rule.condition.initiatorDomain)
        self.assertIn('exoclick.kayako.com', mv3Rule.condition.excludedInitiatorDomain)
        self.assertIn('script', mv3Rule.condition.resourceTypes)
        self.assertIn('sub_frame', mv3Rule.condition.excludedResourceTypes)
        self.assertIn('xmlhttprequest', mv3Rule.condition.excludedResourceTypes)
        self.assertTrue(mv3Rule.condition.isUrlFilterCaseSensitive)

    def test_should_throw_exception_when_caseSensitivity_is_specified_twice(self):
        mv3RuleFactory: Mv3RuleFactory = Mv3RuleFactory()
        unFormattedRule: str = \
            '@@/exoclick/$script,~xmlhttprequest,domain=exoclick.bamboohr.co.uk|~exoclick.kayako.com,~third-party,match-case,match-case'

        self.assertRaises(ParsingError, mv3RuleFactory.createMv3Rule, unFormattedRule, 1)

    def test_should_throw_exception_when_domainOption_is_specified_twice(self):
        mv3RuleFactory: Mv3RuleFactory = Mv3RuleFactory()
        unFormattedRule: str = \
            '@@/exoclick.$script,~xmlhttprequest,domain=exoclick.bamboohr.co.uk|~exoclick.kayako.com,domain=example.com,~third-party'

        self.assertRaises(ParsingError, mv3RuleFactory.createMv3Rule, unFormattedRule, 1)

    def test_should_throw_exception_when_domainType_is_specified_twice(self):
        mv3RuleFactory: Mv3RuleFactory = Mv3RuleFactory()
        unFormattedRule: str = \
            '@@/exoclick.$script,~xmlhttprequest,domain=exoclick.bamboohr.co.uk|~exoclick.kayako.com,~third-party,third-party'

        self.assertRaises(ParsingError, mv3RuleFactory.createMv3Rule, unFormattedRule, 1)

    def test_should_raise_exception_when_regexFilter_is_invalid(self):
        mv3RuleFactory: Mv3RuleFactory = Mv3RuleFactory()

        unFormattedRule1: str = '//$~script,~xmlhttprequest,domain=~exoclick.bamboohr.co.uk|~exoclick.kayako.com'
        unFormattedRule2: str = '/*(a/$~script/,~xmlhttprequest,domain=~exoclick.bamboohr.co.uk|~exoclick.kayako.com'

        self.assertRaises(ParsingError, mv3RuleFactory.createMv3Rule, unFormattedRule1, 1)
        self.assertRaises(re.error, mv3RuleFactory.createMv3Rule, unFormattedRule2, 2)

    def test_should_raise_exception_when_urlFilter_is_invalid(self):
        mv3RuleFactory: Mv3RuleFactory = Mv3RuleFactory()

        unFormattedRule1: str = '$~script,~xmlhttprequest,domain=~exoclick.bamboohr.co.uk|~exoclick.kayako.com'
        unFormattedRule2: str = '||*example.com$~script,~xmlhttprequest,domain=~exoclick.bamboohr.co.uk|~exoclick.kayako.com'

        self.assertRaises(ParsingError, mv3RuleFactory.createMv3Rule, unFormattedRule1, 1)
        self.assertRaises(ParsingError, mv3RuleFactory.createMv3Rule, unFormattedRule2, 2)

    def test_should_raise_exception_when_resourceType_conflict_exists(self):
        mv3RuleFactory: Mv3RuleFactory = Mv3RuleFactory()

        unFormattedRule: str = '||example.com$~script,~xmlhttprequest,xmlhttprequest'

        self.assertRaises(ParsingError, mv3RuleFactory.createMv3Rule, unFormattedRule, 1)


if __name__ == '__main__':
    unittest.main()
