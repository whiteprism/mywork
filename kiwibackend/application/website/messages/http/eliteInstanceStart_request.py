# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class EliteInstanceStartRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.heroLayoutData = []
        self.instanceId = -1
        self.playback = None #PlaybackData
        self.isWin = -1
        self.summary = None #PBBattleSummaryMessage
