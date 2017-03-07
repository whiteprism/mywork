# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class CreateGuildRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.name = ""
        self.icon = -1
        self.limitLevel = -1
        self.category = -1
