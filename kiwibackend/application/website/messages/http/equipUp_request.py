# -*- encoding:utf8 -*-
from messages.http import  BaseHttp
class EquipUpRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.playerEquipId = -1
        self.pos = -1
        self.playerHeroId = -1
