# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class InstanceBoxOpenRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.instanceId = -1
        self.level = -1
        self.category = -1
        
