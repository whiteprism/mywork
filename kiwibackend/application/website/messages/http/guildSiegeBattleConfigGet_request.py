# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class GuildSiegeBattleConfigGetRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.heroIds = []
        self.category = 0
        self.group = 0
        self.power = 0

