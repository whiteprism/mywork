# -*- encoding:utf8 -*-
from messages.http import  BaseHttp
class SettingRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.category = -1
        self.iconId = -1
        self.name = ""
