# -*- encoding:utf8 -*-
from messages.http import  BaseHttp
class PvpOppsResponse(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.opps = []
        self.openState = 1 #1 开启， 2 等待开启中
