# -*- encoding:utf8 -*-
from messages.http import  BaseHttp
class EquipLevelUpRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.deltaLevel = -1
        self.playerEquipId = -1
