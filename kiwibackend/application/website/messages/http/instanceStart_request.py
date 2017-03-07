# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class InstanceStartRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.heroLayoutData = []
        self.instanceId = -1
        self.playback = None #PlaybackData
        self.isWin = False
        self.summary = None #PBBattleSummaryMessage
