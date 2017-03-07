# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class SpeedUpHeroRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.targetPlayerId = -1
        self.category = -1

