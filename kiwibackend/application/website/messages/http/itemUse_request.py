# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class ItemUseRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.count = -1
        self.playerHeroId = -1
        self.playerItemId = -1
        self.selectIndex = 0
