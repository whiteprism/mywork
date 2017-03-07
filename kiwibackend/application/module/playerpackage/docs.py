# -*- coding: utf-8 -*-
from mongoengine import *
from common.docs import PlayerDataBase

class PlayerPackage(PlayerDataBase):
    """
    用户兑换码
    """
    package_name = StringField(unique_with="player_id") #兑换码礼包ID
    package_code = StringField(default="")

    def __unicode__(self):
        return u"%s:%s" %(self.package_name,self.package_code)

