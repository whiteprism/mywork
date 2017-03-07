# -*- encoding:utf8 -*-
from messages.http import  BaseHttp
class LoginBoxRewardRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.activityId = -1
        self.param = -1
