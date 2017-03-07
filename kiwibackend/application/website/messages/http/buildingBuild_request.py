# -*- encoding:utf8 -*-
from messages.http import  BaseHttp
class BuildingBuildRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.centerX = 0
        self.centerY = 0
        self.buildingId = -1
