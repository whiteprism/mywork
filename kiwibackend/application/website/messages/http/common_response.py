# -*- encoding:utf8 -*-
from messages.http import BaseHttp
class CommonResponse(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.activities = None
        self.player = None
        self.conf = None 
        self.notifications = []
        self.serverTime = -1
        self.serverIntCDTime = -1
        self.success = True
        self.errorCode = -1
        self.alertCode = -1
        self.update = None
        self.delete = None
        self.vvv = 0
