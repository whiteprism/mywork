# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class GuildSiegeBattleConfigRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.heroIds = []
        self.powerRanks = []
        self.positions = []
