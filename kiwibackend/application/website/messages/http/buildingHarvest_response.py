# -*- encoding:utf8 -*-
from messages.http import  BaseHttp
class BuildingHarvestResponse(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.diamondCount = -1
        self.playerBuildingId = -1
