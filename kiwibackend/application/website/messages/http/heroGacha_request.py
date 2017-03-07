# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class HeroGachaRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.isTen = False
        self.tavernId = -1
