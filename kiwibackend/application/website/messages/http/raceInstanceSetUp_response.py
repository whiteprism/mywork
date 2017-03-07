# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class RaceInstanceSetUpResponse(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        #self.playback = None #PlaybackData
        self.enemyDatas = None #PlaybackData  enemydata
        self.version = -1
        self.enemies = []
        self.rewards = []
        self.difficulties = []
        self.towerLevel = -1
        self.monsterIds = []
