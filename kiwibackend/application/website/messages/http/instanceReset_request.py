# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class InstanceResetRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.instanceId = -1
        self.category = 1 #1 普通 2 精英
