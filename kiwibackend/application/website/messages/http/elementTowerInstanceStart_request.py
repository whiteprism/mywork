# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class ElementTowerInstanceStartRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.isWin = False
        self.star = 0
        self.levelId = 0
        self.towerId = 0



