# -*- encoding:utf8 -*-
from messages.http import  BaseHttp
class RampartSoldierLevelUpRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.playerRampartSoldierId = -1
