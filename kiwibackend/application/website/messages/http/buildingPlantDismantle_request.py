# -*- encoding:utf8 -*-
from messages.http import  BaseHttp
class BuildingPlantDismantleRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.playerPlantId = -1