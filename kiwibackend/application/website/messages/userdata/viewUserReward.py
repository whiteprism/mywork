# -*- encodings:utf8 -*-
from messages.userdata import BaseUserData
class ViewUserReward(BaseUserData):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.fromHero = False
        self.count = 0
        self.id = 0
        self.level = 0
        self.type = 0 #gid
        self.uid = 0 # player id
