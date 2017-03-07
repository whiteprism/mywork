# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class RaceInstanceSetUpRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.raidId = -1 #活动副本id
        self.instanceId = -1 #难度id
#        self.difficulty = -1
#        self.type = -1
#        self.version = -1

