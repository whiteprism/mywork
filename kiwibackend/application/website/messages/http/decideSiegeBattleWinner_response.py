# -*- encoding:utf8 -*-
from messages.http import  BaseHttp
class DecideSiegeBattleWinnerResponse(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.winner = -1
        self.position = -1
        self.attack_info = None
        self.defence_info = None