# -*- coding: utf-8 -*-
from mongoengine import *
from common.docs import PlayerRedisDataBase, PlayerRedisDataListBase
from common.decorators.memoized_property import memoized_property
from equip.api import get_equip, get_equiprefine,get_equipfragment
from module.common.actionlog import ActionLogWriter
from module.common.static import Static

class PlayerEquip(PlayerRedisDataBase):
    """
    装备
    """
    equip_id = IntField()  #equip id
    playerhero_id = LongField(default=0)  #这个装备被用在哪个英雄身上
    level = IntField(default=1)
    refineLevel = IntField(default=0)
    #refineXp = IntField(default=0)

    @memoized_property
    def equip(self):
        return get_equip(self.equip_id)

    @property
    def obj_id(self):
        return self.equip_id

    def level_up(self, player, level=1):

        for i in range(level):
            self.level += 1
            if self.level == 10:
                player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_ALL_EQUIP_ENHANCE10, number=1, is_incr=True,with_top=False, is_series=True)
            elif self.level == 20:
                player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_ALL_EQUIP_ENHANCE20, number=1, is_incr=True, with_top=False, is_series=True)
            elif self.level == 30:
                player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_ALL_EQUIP_ENHANCE30, number=1, is_incr=True, with_top=False, is_series=True)
            elif self.level == 40:
                player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_ALL_EQUIP_ENHANCE40, number=1, is_incr=True, with_top=False, is_series=True)

    def refine(self, level =1):
        """
        装备精炼
        """
        self.refineLevel += level

    @property
    def can_melt(self):
        return not (self.level == 1 and self.refineLevel == 0)

    def melt(self):
        self.level = 1
        self.refineLevel = 0
        self.refineXp = 0

    @property
    def can_decompose(self):
            return self.playerhero_id == 0

    #def get_slot(self, pos):
    #    """
    #    获取对应插槽位置的宝石id
    #    """
    #    if not hasattr(self, "slot%sGid" % pos):
    #        return 0

    #    return getattr(self, "slot%sGid" % pos)


    #def slot_in(self, pos, gem_id):
    #    """
    #    镶嵌宝石
    #    """
    #    if not hasattr(self, "slot%sGid" % pos):
    #       return False

    #    if getattr(self, "slot%sGid" % pos):
    #        return False

    #    setattr(self, "slot%sGid" % pos, gem_id)
        
    #    return True

    #def can_upgrade(self):
    #    """
    #    检查是否可以进阶
    #    """
    #   for i in range(0, len(self.equip.gemList)):
    #        if not self.get_slot(i):
    #            return False
    #    return True

    #def upgrade(self, new_equip):
    #    """
    #    装备进阶
    #    """
    #    self.equip_id = new_equip.id
    #    for i in range(0, len(self.equip.gemList)):
    #        setattr(self, "slot%sGid" % i, 0)
    #
    #   return True

    #@property
    #def is_binding(self):
    #    return self.binding_playerhero_id > 0

    #def binding(self, playerhero):
    #    self.binding_playerhero_id = playerhero.pk

    #def unbinding(self):
    #    self.binding_playerhero_id = 0

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["equipId"] = self.equip_id
        dicts["heroId"] = self.playerhero_id
        #dicts["bindingHeroId"] = self.binding_playerhero_id

        del dicts["equip_id"]
        del dicts["playerhero_id"]
        #del dicts["binding_playerhero_id"]
        return dicts

class PlayerEquipFragment(PlayerRedisDataListBase):
    """
    用户装备碎片
    """
    @memoized_property
    def equipfragment(self):
        return get_equipfragment(self.equipfragment_id)

    @property
    def equipfragment_id(self):
        return self.obj_id

    @property
    def is_equipfragment(self):
        return True
        
    def sub(self,delta_number=1, info=u""):
        """
        使用装备碎片
        """
        before_number = self.count
        self.count -= delta_number
        if self.display:
            self.player.update_equipfragment(self, True)
        else:
            self.player.delete_equipfragment(self.equipfragment_id, True)

        ActionLogWriter.equipfragment_cost(self.player, self.equipfragment, before_number, self.count, info)

    def add(self,delta_number=1, info=u""):
        before_number = self.count
        self.count += delta_number
        after_number = self.count

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["equipFragmentId"] = self.obj_id
        return dicts
