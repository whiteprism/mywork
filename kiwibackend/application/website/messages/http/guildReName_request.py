# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class GuildReNameRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.name = ""
        self.level = -1
