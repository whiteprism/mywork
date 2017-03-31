# -*- coding: utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler
from rewards.models import RewardsBase
from common.decorators.memoized_property import memoized_property
from module.common.static import Static
from module.instance.api import get_triggerinfo

class PVPRank(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"竞技场排行"
    name = models.CharField(u"名称", default="", max_length=40)
    titleID = models.CharField(u"ID", default="", max_length=200)
    score = models.IntegerField(u"积分", default=0)
    rank = models.IntegerField(u"排名", default=0)
    weeklyRewards_int = models.CharField(u"奖励", default="", max_length=200)
    dailyRewards_int = models.CharField(u"每日排行奖励", default="", max_length=200)

    def __unicode(self):
        return "%s" % self.pk

    @memoized_property
    def weeklyRewards(self):
        return [PVPReward.get(pk) for pk in self.weeklyRewards_int.strip().split(",") if pk]

    @memoized_property
    def dailyRewards(self):
        return [PVPReward.get(pk) for pk in self.dailyRewards_int.strip().split(",") if pk]

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["weeklyRewards"] = [weeklyReward.to_dict() for weeklyReward in self.weeklyRewards]
        dicts["dailyRewards"] = [dailyReward.to_dict() for dailyReward in self.dailyRewards]

        dicts["pk"] = self.pk

        del dicts["name"]
        del dicts["id"]
        return dicts

class PVPUpgradeScore(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"积分段位表"
    rewards_int = models.CharField(u"奖励", default="", max_length=200)
    mulLang = models.CharField(u"邮件多语言", default="", max_length=200)
    upgrade = models.CharField(u"段位描述多语言", default="", max_length=200)
    def __unicode(self):
        return "%s" % self.pk

    @memoized_property
    def rewards(self):
        return [PVPReward.get(pk) for pk in self.rewards_int.strip().split(",") if pk]

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["rewards"] = [reward.to_dict() for reward in self.rewards]

        del dicts["id"]
        return dicts

class PVPReward(RewardsBase):
    SHEET_NAME = u"竞技场排行奖励"

class PVPScene(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"PVP场景"
    scene = models.CharField(u"场景", default="", max_length=200)
    startPoints_int = models.CharField(u"集结点", default="", max_length=200)
    zoneID = models.IntegerField(u"区域ID", default=0)
    triggerInfos_int = models.CharField(u"触发器", max_length=500, default="")

    @memoized_property
    def triggerInfos(self):
        if self.triggerInfos_int.strip():
            return [get_triggerinfo(int(float(pk))) for pk in self.triggerInfos_int.strip().split(",") if pk]
        return []

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = self.id
        dicts["triggerInfos"] = [triggerInfo.to_dict() for triggerInfo in self.triggerInfos]
        del dicts["id"]
        return dicts

class SiegeRandomNumber(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"攻城战随机数"
    number = models.FloatField(u"攻城战随机数", default=0)

