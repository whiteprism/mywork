# -*- encoding:utf8 -*-
from messages.http import  BaseHttp
class TaskRewardRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.taskId = -1
