import re
from typing import List


class OptionValidator:
     def __init__(self):
         self.resourceTypeValues: List[str] = [ 'script','image', 'stylesheet', 'object', 'xmlhttprequest',
                                                'subdocument', 'ping', 'websocket', 'webrtc' , 'document' ,
                                                '~script', '~image', '~stylesheet', '~object', '~xmlhttprequest',
                                                '~subdocument', '~ping', '~websocket', '~webrtc', '~document',
                                                '~elemhide','~other''elemhide' , 'popup', 'font' , 'media' , 'other']
         self.domainTypeValues: List[str] = ['third-party', '~third-party']

     def optionIsAVResourceType(self, aValue: str):
         if aValue in self.resourceTypeValues:
             return True
         return False

     def optionIsAValidDomainType(self, aValue: str):
         if aValue in self.domainTypeValues:
             return True
         return False

     def optionIsAInitiatorDomain(self, aValue: str):
         pattern: str = r'^domain='
         if re.match(pattern, aValue):
             return True
         return False
