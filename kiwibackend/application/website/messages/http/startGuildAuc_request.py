# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class StartGuildAucRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()

        self.price = -1
        self.aucRewardId = -1
