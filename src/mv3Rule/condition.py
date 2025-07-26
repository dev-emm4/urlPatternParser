import re
from typing import List
from src.optionValidator import OptionValidator

class Condition:
    def __init__(self):
        self.urlFilter: None | str = None
        self.regexFilter: None | str = None
        self.domainType: None | str = None
        self.initiatorDomain: None | List[str] = None
        self.excludedInitiatorDomain: None | List[str] = None
        self.resourceType: None | List[str] = None
        self.excludedResourceType: None | List[str] = None
        self.optionValidator: OptionValidator = OptionValidator()
