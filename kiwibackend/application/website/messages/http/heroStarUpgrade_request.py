# -*- encoding:utf8 -*-
from messages.http import  BaseHttp
class HeroStarUpgradeRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.playerHeroId = -1
        self.useSoulFirst = True
