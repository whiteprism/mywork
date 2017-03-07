# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class GuildFireBuffSettingsRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.buffType = -1
        self.buffLevel = -1
        self.index = -1
        self.hour = -1