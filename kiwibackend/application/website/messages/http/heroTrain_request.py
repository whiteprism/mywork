# -*- encoding:utf8 -*-
from messages.http import  BaseHttp
class HeroTrainRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.playerHeroId = -1
        self.trainType = 0
        self.count = 0
