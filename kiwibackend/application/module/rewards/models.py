# -*- coding: utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler
from common.decorators.memoized_property import memoized_property

class RewardCls(object):
    """
    基类
    """
    type  = 0
    count = 0
    level = 0

    @memoized_property
    def equip(self):
        from module.equip.api import get_equip
        return get_equip(self.type)

    @memoized_property
    def equipfragment(self):
        from module.equip.api import get_equipfragment
        return get_equipfragment(self.type)

    @memoized_property
    def artifact(self):
        from module.artifact.api import get_artifact
        return get_artifact(self.type)

    @memoized_property
    def buildingfragment(self):
        from module.building.api import get_buildingfragment
        return get_buildingfragment(self.type)

    @memoized_property
    def soul(self):
        from module.soul.api import get_soul
        return get_soul(self.type)

    @memoized_property
    def artifactfragment(self):
        from module.artifact.api import get_artifactfragment
        return get_artifactfragment(self.type)

    @memoized_property
    def item(self):
        from module.item.api import get_item
        return get_item(self.type)

    @property
    def name(self):
        if self.is_hero:
            return ""
        elif self.is_equip:
            return self.equip.nameId
        elif self.is_equipfragment:
            return self.equipfragment.nameId
        elif self.is_artifact:
            return self.artifact.nameId
        elif self.is_buildingfragment:
            return self.buildingfragment.nameId
        elif self.is_soul:
            return self.soul.nameId
        elif self.is_item:
            return self.item.nameId
        elif self.is_artifactfragment:
            return self.artifactfragment.nameId
        elif self.is_tower:
            return "fytext_421"
        elif self.is_gold:
            return "fytext_20029"
        elif self.is_wood:
            return "fytext_20037"
        elif self.is_yuanbo:
            return "fytext_308"
        elif self.is_couragepoint:
            return "fytext_20031"
        elif self.is_honorpoint:
            return "fytext_20032"
        elif self.is_xp:
            return "fytext_20034"
        elif self.is_power:
            return "fytext_20035"
        elif self.is_guildgold:
            return "fytext_20033"

    @property
    def is_hero(self):
        return self.get_idType(self.type) == 11

    @property
    def is_equip(self):
        return self.get_idType(self.type) == 12

    @property
    def is_artifact(self):
        return self.get_idType(self.type) == 14

    @property
    def is_buildingfragment(self):
        return self.get_idType(self.type) == 15
        
    @property
    def is_army(self):
        return self.get_idType(self.type) == 19

    @property
    def is_soul(self):
        return self.get_idType(self.type) == 20


    @property
    def is_equipfragment(self):
        return self.get_idType(self.type) == 23

    @property
    def is_artifactfragment(self):
        return self.get_idType(self.type) == 24

    @property
    def is_item(self):
        return self.get_idType(self.type) == 26

    @property
    def is_tower(self):
        return self.get_idType(self.type) == 71

    @property
    def is_gold(self):
        return self.get_idType(self.type) == 50

    @property
    def is_wood(self):
        return self.get_idType(self.type) == 60

    @property
    def is_yuanbo(self):
        return self.get_idType(self.type) == 51

    @property
    def is_couragepoint(self):
        return self.get_idType(self.type) == 52

    @property
    def is_honorpoint(self):
        return self.get_idType(self.type) == 53


    @property
    def is_xp(self):
        return self.get_idType(self.type) == 55

    @property
    def is_power(self):
        return self.get_idType(self.type) == 56

    @property
    def is_stamina(self):
        return self.get_idType(self.type) == 58

    @property
    def is_guildgold(self):
        return self.get_idType(self.type) == 77

    def get_idType(self, Id):
        return int(str(Id)[0:2])


class RewardsBase(models.Model, RewardCls, StaticDataRedisHandler, CommonStaticModels):
    count = models.IntegerField(u"count",default=0)
    level = models.IntegerField(u"level",default=0)
    type = models.IntegerField(u"type",default=0)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"%s:%s:%s:%s" %(self.pk, self.level, self.type, self.count)

    def to_dict(self):
        dicts = super(RewardsBase, self).to_dict()
        del dicts["id"]
        return dicts


    
class CommonReward(RewardCls):
    """
    通用副本
    """

    def __init__(self, type, count, level):
        '''
        构造函数
        '''
        self.type = type
        self.count = count
        self.level = level

    def __unicode__(self):
        return u"%s:%s:%s" %(self.type, self.count, self.level)

    def to_dict(self):
        dicts = {}
        dicts["type"] = self.type
        dicts["level"] = self.level
        dicts["count"] = self.count
        return dicts
