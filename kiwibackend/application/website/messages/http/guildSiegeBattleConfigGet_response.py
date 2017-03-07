# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class GuildSiegeBattleConfigGetResponse(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.leftInfo = []
        self.middInfo = []
        self.rightInfo = []
        self.leftLength = -1
        self.rightLength = -1
        self.middleLength = -1
