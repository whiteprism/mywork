# -*- coding: utf-8 -*-
from mongoengine import *
from common.docs import PlayerRedisDataListBase
from module.common.actionlog import ActionLogWriter
from module.soul.api import get_soul
from common.decorators.memoized_property import memoized_property

class PlayerSoul(PlayerRedisDataListBase):
    '''
    用户HERO魂魄
    '''
    from_hero = False

    @memoized_property
    def soul(self):
        return get_soul(self.soul_id)

    @property
    def is_hero(self):
        return False

    @property
    def is_soul(self):
        return True

    @property
    def soul_id(self):
        return self.obj_id

    def sub(self,number, info=""):
        """
        消耗魂魄
        """
        before_number = self.count
        self.count -= number
        after_number = self.count 

        ActionLogWriter.soul_cost(self.player, self.obj_id, before_number, after_number, info)

        if self.display:
            self.player.update_soul(self, True)
        else:
            self.player.delete_soul(self.pk, True)

    def add(self, delta_number=1, info=u""):
        """
        获取魂魄
        """
        before_number = self.count 
        self.count += delta_number
        after_number = self.count 
        ActionLogWriter.soul_add(self.player, self.obj_id, before_number, after_number, info)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["soulId"] = self.obj_id
        return dicts
