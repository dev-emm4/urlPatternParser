import unittest
from src.mv3Rule.mv3RuleFactory import Mv3RuleFactory
from src.mv3Rule.mv3Rule import Mv3Rule

class Mv3RuleFactoryTestCase(unittest.TestCase):
    def test_shouldCreateBlockingMv3Rule(self):
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



if __name__ == '__main__':
    unittest.main()
