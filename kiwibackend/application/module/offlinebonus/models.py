# -*- coding: utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler
#from rewards.models import RewardsBase
from common.decorators.memoized_property import memoized_property

# class OfflineBonusBase(models.Model, StaticDataRedisHandler, CommonStaticModels):
#     SHEET_NAME = u"离线奖励"
#     lev_add = models.IntegerField(u"等级加成",default=0)
#     day_add = models.IntegerField(u"离线天数加成",default=0)
    # offlinedays = models.IntegerField(u"消耗荣誉点",default=0)
    # rewardIds_str = models.CharField(u"奖励", max_length=200, default="")

    # @memoized_property
    # def rewards(self):
    #     from rewards.api import get_commonreward
    #     return [get_commonreward(pk) for pk in self.rewardIds_str.strip().split(",") if pk]

class OfflineBonusLevel(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"离线等级奖励"
    rewardIds_str = models.CharField(u"奖励ID", max_length=100, default=0)

    @memoized_property
    def rewards(self):
        from rewards.api import get_commonreward
        return [get_commonreward(pk) for pk in self.rewardIds_str.strip().split(",") if pk]


class OfflineBonusDay(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"离线天数奖励"
    rewardIds_str = models.CharField(u"奖励ID", max_length=100, default=0)

    @memoized_property
    def rewards(self):
        from rewards.api import get_commonreward
        return [get_commonreward(pk) for pk in self.rewardIds_str.strip().split(",") if pk]
