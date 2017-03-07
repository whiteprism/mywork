# -*- encoding:utf8 -*-
from messages.http import  BaseHttp
class PvpEnemyDataResponse(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.artifacts = []
        self.equips = []
        self.heros = []
        self.user = None #PBViewUserSimple
