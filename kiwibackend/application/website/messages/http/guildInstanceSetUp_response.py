# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class GuildInstanceSetUpResponse(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.enemies = []
        self.bossHp = -1
        self.bossPercentage = -1
