# -*- encoding: utf8 -*-
from messages.http import  BaseHttp
class GuildShopInitRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.category = -1
