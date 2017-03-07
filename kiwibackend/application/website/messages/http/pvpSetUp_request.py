# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class PvpSetUpRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.oppId = 0
        self.category = -1 #0:竞技场 1：掠夺
