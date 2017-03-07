# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class GuildInstanceStartRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.instanceId = -1
        self.isWin = -1
        self.bossHp = -1
        self.bossPercentage = 0.0
