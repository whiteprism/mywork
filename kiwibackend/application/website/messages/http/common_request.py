# -*- encoding:utf8 -*-
from messages.http import  BaseHttp
class CommonRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.channel = ""
        self.client = ""
        #self.confVersion = -1
        #self.instanceMd5 = ""
        self.seed = ""
        self.powerRank = 0
        self.maxFiveHeroPower = 0
        self.sessionId = ""
        self.playerId = -1
        self.packageVersion = ""
        self.deviceId = ""
        self.bundleVersion = -1
        self.clientTime = -1
        self.vvv = 0
        self.serverid = 0
