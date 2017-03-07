# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class RaceInstanceStartRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.raidId = -1 #活动副本id
        self.instanceId = -1 #难度的id
        self.heroLayoutData = []
        self.playback = None #PlaybackData
        self.isWin = -1
        self.summary = None #PBBattleSummaryMessage
        self.waveCount = 0
        self.heroInfos = []
        self.percentage = 0.0
        self.star = -1

