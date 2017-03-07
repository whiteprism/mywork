# -*- encoding:utf8 -*-
from messages.http import  BaseHttp
class SmallGameFinishRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.score = -1