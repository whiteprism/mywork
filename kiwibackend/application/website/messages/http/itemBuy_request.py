# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class ItemBuyRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.count = -1
        self.storeItemId = -1
