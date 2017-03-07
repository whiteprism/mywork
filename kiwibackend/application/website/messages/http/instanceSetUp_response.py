# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class InstanceSetUpResponse(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.enemies = None #PlaybackData
        self.specialBattle = False
        self.rewards = []
        self.version = 0
