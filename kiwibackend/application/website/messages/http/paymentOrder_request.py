# -*- encoding:utf8 -*-
from messages.http import  BaseHttp
class PaymentOrderRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.channel = ""
        self.diamondId = -1
        self.channelUserId = ""
