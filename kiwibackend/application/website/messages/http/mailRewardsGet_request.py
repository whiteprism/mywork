# -*- encoding:utf8 -*-
from messages.http import  BaseHttp
class MailRewardsGetRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.mailId = -1
