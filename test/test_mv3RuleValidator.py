import unittest

from src.mv3Rule.mv3Rule import Mv3Rule
from src.mv3Rule.mv3RuleFactory import Mv3RuleFactory
from src.mv3RuleValidator import Mv3RuleValidator

class Mv3RuleValidatorTestCase(unittest.TestCase):
    def test_should_raise_exception_when_regexFilter_is_invalid(self):
        mv3RuleValidator: Mv3RuleValidator = Mv3RuleValidator()
        mv3RuleFactory: Mv3RuleFactory = Mv3RuleFactory()

        unFormattedRule1: str = '//$~script,~xmlhttprequest,domain=~exoclick.bamboohr.co.uk|~exoclick.kayako.com'
        unFormattedRule2: str = '/*(a/$~script/,~xmlhttprequest,domain=~exoclick.bamboohr.co.uk|~exoclick.kayako.com'

        mv3Rule1: Mv3Rule = mv3RuleFactory.createMv3Rule(unFormattedRule1, 1)
        mv3Rule2: Mv3Rule = mv3RuleFactory.createMv3Rule(unFormattedRule2, 2)


        self.assertRaises(Exception, mv3RuleValidator.validate, mv3Rule1)
        self.assertRaises(Exception, mv3RuleValidator.validate, mv3Rule2)

    def test_should_raise_exception_when_urlFilter_is_invalid(self):
        mv3RuleValidator: Mv3RuleValidator = Mv3RuleValidator()
        mv3RuleFactory: Mv3RuleFactory = Mv3RuleFactory()

        unFormattedRule1: str = '$~script,~xmlhttprequest,domain=~exoclick.bamboohr.co.uk|~exoclick.kayako.com'
        unFormattedRule2: str = '||*$~script,~xmlhttprequest,domain=~exoclick.bamboohr.co.uk|~exoclick.kayako.com'

        mv3Rule1: Mv3Rule = mv3RuleFactory.createMv3Rule(unFormattedRule1, 1)
        mv3Rule12: Mv3Rule = mv3RuleFactory.createMv3Rule(unFormattedRule2, 2)

        self.assertRaises(Exception, mv3RuleValidator.validate, mv3Rule1)
        self.assertRaises(Exception, mv3RuleValidator.validate, mv3Rule12)

    def test_should_raise_exception_when_resourceType_conflict_exists(self):
        mv3RuleValidator: Mv3RuleValidator = Mv3RuleValidator()
        mv3RuleFactory: Mv3RuleFactory = Mv3RuleFactory()

        unFormattedRule: str = '||example.com$~script,~xmlhttprequest,xmlhttprequest'

        mv3Rule: Mv3Rule = mv3RuleFactory.createMv3Rule(unFormattedRule, 1)

        self.assertRaises(Exception, mv3RuleValidator.validate, mv3Rule)



if __name__ == '__main__':
    unittest.main()
