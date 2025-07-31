import unittest
from src.mv3Rule.mv3RuleFactory import Mv3RuleFactory
from src.mv3Rule.mv3Rule import Mv3Rule

class Mv3RuleFactoryTestCase(unittest.TestCase):
    def test_should_create_blocking_Mv3Rule(self):
        mv3RuleFactory: Mv3RuleFactory = Mv3RuleFactory()
        unFormattedRule: str = '/exoclick.$~script,~xmlhttprequest,domain=~exoclick.bamboohr.co.uk|~exoclick.kayako.com'
        mv3Rule: Mv3Rule = mv3RuleFactory.createMv3Rule(unFormattedRule, 1)

        self.assertEqual(mv3Rule.id, 1)
        self.assertEqual(mv3Rule.priority, 1)
        self.assertEqual(mv3Rule.condition.urlFilter, '/exoclick.')
        self.assertEqual(mv3Rule.condition.domainType, None)
        self.assertEqual(mv3Rule.action.type, 'block')
        self.assertIn('exoclick.bamboohr.co.uk' ,mv3Rule.condition.excludedInitiatorDomain)
        self.assertIn('exoclick.kayako.com', mv3Rule.condition.excludedInitiatorDomain)
        self.assertIn('xmlhttprequest', mv3Rule.condition.excludedResourceType)
        self.assertIn('script', mv3Rule.condition.excludedResourceType)

    def test_should_create_allowing_Mv3Rule(self):
        mv3RuleFactory: Mv3RuleFactory = Mv3RuleFactory()
        unFormattedRule: str = '@@/exoclick/$script,~xmlhttprequest,domain=exoclick.bamboohr.co.uk|~exoclick.kayako.com,~third-party'
        mv3Rule: Mv3Rule = mv3RuleFactory.createMv3Rule(unFormattedRule, 1)

        self.assertEqual(mv3Rule.id, 1)
        self.assertEqual(mv3Rule.priority, 2)
        self.assertEqual(mv3Rule.condition.regexFilter, '/exoclick/')
        self.assertEqual(mv3Rule.condition.domainType, 'firstParty')
        self.assertEqual(mv3Rule.action.type, 'allow')
        self.assertIn('exoclick.bamboohr.co.uk', mv3Rule.condition.initiatorDomain)
        self.assertIn('exoclick.kayako.com', mv3Rule.condition.excludedInitiatorDomain)
        self.assertIn('script', mv3Rule.condition.resourceType)
        self.assertIn('xmlhttprequest', mv3Rule.condition.excludedResourceType)

    def test_should_throw_exception_when_domainOption_is_specified_twice(self):
        mv3RuleFactory: Mv3RuleFactory = Mv3RuleFactory()
        unFormattedRule: str = '@@/exoclick.$script,~xmlhttprequest,domain=exoclick.bamboohr.co.uk|~exoclick.kayako.com,domain=example.com,~third-party'

        self.assertRaises(Exception, mv3RuleFactory.createMv3Rule, [unFormattedRule, 1])

    def test_should_throw_exception_when_domainType_is_specified_twice(self):
        mv3RuleFactory: Mv3RuleFactory = Mv3RuleFactory()
        unFormattedRule: str = '@@/exoclick.$script,~xmlhttprequest,domain=exoclick.bamboohr.co.uk|~exoclick.kayako.com, ~third-party, third-party'

        self.assertRaises(Exception, mv3RuleFactory.createMv3Rule, [unFormattedRule, 1])


if __name__ == '__main__':
    unittest.main()
