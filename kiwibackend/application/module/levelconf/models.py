#-*- coding:utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler
from rewards.models import RewardsBase
from common.decorators.memoized_property import memoized_property

class LevelConf(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"升级配置"
    battleLeftDownX = models.IntegerField(u"开格子", default=0)
    battleLeftDownY = models.IntegerField(u"开格子", default=0)
    battleRightTopX = models.IntegerField(u"开格子", default=0)
    battleRightTopY = models.IntegerField(u"开格子", default=0)
    energy = models.IntegerField(u"体力", default=0)
    levelUpRewards_int = models.CharField(u"升级奖励列表", max_length = 200, default="")
    rewardPower = models.IntegerField(u"奖励体力", default=0)
    rewardStamina = models.IntegerField(u"奖励的耐力", default=0)
    stamina = models.IntegerField(u"耐力", default=0)
    battlePoint = models.IntegerField(u"战斗点", default=0)
    wallHp = models.IntegerField(u"墙血", default=0)
    xp = models.IntegerField(u"经验上限", default=0)
    unlockIconId = models.IntegerField(u"解锁ICON", default=0) 

    def __unicode__(self):
        return u"%s" % self.pk

    class Meta:
        ordering = ["id"]

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = dicts["id"]
        dicts["levelUpRewards"] = [reward.to_dict() for reward in self.levelUpRewards]
        del dicts["id"]
        return dicts

    @memoized_property
    def levelUpRewards(self):
        return [LevelUpReward.get(pk) for pk in self.levelUpRewards_int.strip().split(",") if pk]

class LevelUpReward(RewardsBase):
    SHEET_NAME = u"升级奖励"
