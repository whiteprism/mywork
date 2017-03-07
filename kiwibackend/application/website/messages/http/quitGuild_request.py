# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class QuitGuildRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.id = -1
