# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class GuildInstanceCancelRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.instanceId = -1

