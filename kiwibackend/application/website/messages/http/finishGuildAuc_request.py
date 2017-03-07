# -*- encoding:utf8 -*-
from messages.http import  BaseHttp
class FinishGuildAucRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.price = -1
        self.instanceId = -1
        self.itemId = -1
        self.category = -1
