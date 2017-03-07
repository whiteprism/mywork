# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class InstanceSweepRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.count = -1
        self.category = -1
        self.instanceId = -1

