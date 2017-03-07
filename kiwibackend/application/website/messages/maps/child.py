# -*- encoding:utf8 -*-
from messages.maps import BaseMap
class ChildMap(BaseMap):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.commonRequest = None #PBCommonRequest
        self.commonResponse = None #PBCommonResponse
        self.request = None #PBLoginMessage_PBRequest
        self.response = None #PBLoginMessage_PBResponse
