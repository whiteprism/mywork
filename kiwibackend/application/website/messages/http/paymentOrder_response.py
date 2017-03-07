# -*- encoding:utf8 -*-
from messages.http import  BaseHttp
class PaymentOrderResponse(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.orderId = ""
