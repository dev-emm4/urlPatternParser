import unittest

from mv3Rule.action import Action
from mv3Rule.condition import Condition
from mv3Rule.mv3Rule import Mv3Rule


class Mv3RUleTestCase(unittest.TestCase):
    def setUp(self):
        self.action: Action = Action('block')
        self.condition: Condition = self._generate_condition(
            'example.com', 'thirdParty', 'example.com', 'any.com',
            'document', 'script')
        self.mv3Rule = Mv3Rule(1, 1, self.action, self.condition)
        self.expectedRule = self._expectedRule()

    def test_should_transform_mv3Rule_to_dict(self):
        dictMv3Rule = self.mv3Rule.to_dict()

        self.assertEqual(self.mv3Rule.to_dict(), self.expectedRule)

    def _generate_condition(self, aUrlFilter: str, aDomainType: str, aInitiatorDomain: str,
                            aExcludedInitiatorDomain: str, aResourceType: str,
                            aExcludedResourceType: str) -> Condition:
        condition: Condition = Condition()
        condition.setUrlFilter(aUrlFilter)
        condition.setDomainType(aDomainType)
        condition.includeInitiatorDomain(aInitiatorDomain)
        condition.excludeInitiatorDomain(aExcludedInitiatorDomain)
        condition.includeResourceType(aResourceType)
        condition.excludeResourceType(aExcludedResourceType)
        condition.activateCaseSensitivity()

        return condition

    def _expectedRule(self):
        expectedRule = {
            'id': 1,
            'priority': 1,
            'action': {'type': 'block'},
            'condition': {'urlFilter': 'example.com',
                          'domainType': 'thirdParty',
                          'initiatorDomain': ['example.com'],
                          'excludedInitiatorDomain': ['any.com'],
                          'resourceTypes': ['document'],
                          'excludedResourceTypes': ['script'],
                          'isUrlFilterCaseSensitive': True}}

        return expectedRule


if __name__ == '__main__':
    unittest.main()
