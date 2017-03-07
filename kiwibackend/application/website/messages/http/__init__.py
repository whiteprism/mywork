# -*- encoding:utf8 -*-
from messages import BaseMessage
class BaseHttp(BaseMessage):
    def __init__(self):
        super(BaseHttp, self).__init__()
        self.timeDelay = False
