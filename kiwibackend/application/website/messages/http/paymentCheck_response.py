# -*- encoding:utf8 -*-
from messages.http import  BaseHttp
class PaymentCheckResponse(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.result = False
        self.diamond = -1
        self.isFirst = False
