# -*- encoding:utf8 -*-
from messages.http import  BaseHttp
class PvpStartRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.isWin = False
        self.playback = []
        self.layout = [] #PBViewLayout
        self.oppId = -1
        self.summary = [] #PBBattleSummaryMessage
        self.fragmentId = 0 # 神器碎片id
        self.powerRank = 0 #战斗力
        self.pvpType = 0
        self.fortIndexes = []
