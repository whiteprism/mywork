# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class SearchGuildRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.guildParam = ""
        self.category = -1
