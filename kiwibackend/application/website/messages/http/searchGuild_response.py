# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class SearchGuildResponse(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.result = []
        self.category = -1
