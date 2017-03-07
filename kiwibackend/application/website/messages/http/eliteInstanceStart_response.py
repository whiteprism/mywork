# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class EliteInstanceStartResponse(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.heroLevelUp = []
        self.playback = None #PlaybackData
        self.rewards = []
        self.summary = None #PBBattleSummaryMessage
        self.star = 0
