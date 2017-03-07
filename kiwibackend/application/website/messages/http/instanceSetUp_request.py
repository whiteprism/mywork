# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class InstanceSetUpRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.instanceId = -1
        self.version = 0
