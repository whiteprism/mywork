# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class EliteInstanceSetUpResponse(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.enemies = None #PlaybackData  enemydata
        self.rewards = []