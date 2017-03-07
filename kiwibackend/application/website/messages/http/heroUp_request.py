# -*- encoding:utf8 -*-
from messages.http import  BaseHttp
class HeroUpRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.from_hero = -1
        self.to_hero = -1
        self.pos = -1
