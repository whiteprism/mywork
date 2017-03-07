# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class PvpSetUpResponse(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.playback = None #PlaybackData
        self.category = 0 #0:竞技场 1:掠夺
        self.openState = 1 #1 正常开启， 2 结算中，等待开启
        self.pvpSceneId = 0
