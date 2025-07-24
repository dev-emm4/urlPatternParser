import unittest
from  src.mv3Rule.condition import  Condition


class conditionTestCase(unittest.TestCase):
    def test_should_register_domainType_as_firstParty(self):
        condition: Condition = Condition()
        condition.registerDomainType('~third-party')
        self.assertEqual(condition.domainType, 'firstParty')

    def test_should_register_domainType_as_thirdParty(self):
        condition: Condition = Condition()
        condition.registerDomainType('third-party')
        self.assertEqual(condition.domainType, 'thirdParty')

    def test_should_throwException_if_DomainType_is_invalid(self):
        condition: Condition = Condition()
        self.assertRaises(Exception, condition.registerDomainType, 'fourth-party')

    def test_should_throwsException_if_domainType_is_registered_twice(self):
        condition: Condition = Condition()
        condition.registerDomainType('third-party')
        self.assertRaises(Exception, condition.registerDomainType, 'first-party')

    def test_should_register_excludedInitiatorDomain(self):
        condition: Condition = Condition()
        condition.registerInitiatorDomain('~adtrack.ca|~adtrack.yacast.fr')
        # Ensuring excludedInitiatorDomain was set
        self.assertIn('adtrack.ca', condition.excludedInitiatorDomain)
        self.assertIn('adtrack.yacast.fr', condition.excludedInitiatorDomain)
        # Ensuring initiatorDomain was not set
        self.assertIsNone(condition.initiatorDomain)

    def test_should_register_initiatorDomain(self):
        condition: Condition = Condition()
        condition.registerInitiatorDomain('adtrack.ca|adtrack.yacast.fr')
        # Ensuring initiatorDomain was set
        self.assertIn('adtrack.ca', condition.initiatorDomain)
        self.assertIn('adtrack.yacast.fr', condition.initiatorDomain)
        # Ensuring excludedInitiatorDomain was not set
        self.assertIsNone(condition.excludedInitiatorDomain)

    def test_should_register_excludedInitiatorDomain_and_initiatorDomain(self):
        condition: Condition = Condition()
        condition.registerInitiatorDomain('~adtrack.ca|adtrack.yacast.fr')
        # Ensuring initiatorDomain was set
        self.assertIn('adtrack.ca', condition.excludedInitiatorDomain)
        self.assertIn('adtrack.yacast.fr', condition.initiatorDomain)

    def test_should_throwsException_if_excluded_or_initiatorDomain_is_registered_twice(self):
        condition: Condition = Condition()
        condition.registerInitiatorDomain('~adtrack.ca|adtrack.yacast.fr')
        # re-registering initiatorDomain and excludedInitiatorDomain
        self.assertRaises(Exception, condition.registerInitiatorDomain, 'adtrack.ca|~adtrack.yacast.fr')

    def test_should_throwsException_if_duplicate_domainName_exists(self):
        condition: Condition = Condition()
        # ~adtrack.ca and adtrack.ca are duplicate domain names
        self.assertRaises(Exception, condition.registerInitiatorDomain, '~adtrack.ca|adtrack.ca|adtrack.yacast.fr')

    def test_should_register_empty_string_as_initiatorDomain(self):
        condition: Condition = Condition()
        condition.registerInitiatorDomain('~example.com|')
        # Ensuring initiatorDomain was set
        self.assertIn('example.com', condition.excludedInitiatorDomain)
        self.assertIn('', condition.initiatorDomain)

    def test_should_register_urlFilter(self):
        condition: Condition = Condition()
        condition.registerPattern('||example.com^')
        # Ensuring urlFilter was set
        self.assertEqual(condition.urlFilter, '||example.com^')
        # Ensuring regexFilter was not set
        self.assertIsNone(condition.regexFilter)

    def test_should_register_regexFilter(self):
        condition: Condition = Condition()
        condition.registerPattern('/example.com/')
        # Ensuring regexFilter was set
        self.assertEqual(condition.regexFilter, '/example.com/')
        # Ensuring urlFilter was not set
        self.assertIsNone(condition.urlFilter)

    def test_should_throwException_if_pattern_is_registered_twice(self):
        condition: Condition = Condition()
        condition.registerPattern('/example.com/')
        # re-registering pattern
        self.assertRaises(Exception, condition.registerPattern, '/example.com/')
        self.assertRaises(Exception, condition.registerPattern, '||example.com^')

    # def test_should_register_resourceType(self):
    #     condition: Condition = Condition()
    #     condition.setResource('script')
















if __name__ == '__main__':
    unittest.main()
