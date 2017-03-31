# -*- coding: utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler
from rewards.models import RewardsBase
from rewards.api import get_commonreward
from common.decorators.memoized_property import memoized_property

class Vip(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"VIP"
    diamond = models.IntegerField(u"每个等级充值额度", default=0)
    sweepCount = models.IntegerField(u"扫荡券数量", default=0)
    refreshMysteryShopCount = models.IntegerField(u"神秘商店免费刷新", default=0)
    buyPowerCount = models.IntegerField(u"体力购买次数", default=0)
    buyGoldBoxCount = models.IntegerField(u"金宝箱购买次数", default=0)
    buyStaminaCount = models.IntegerField(u"耐力购买次数", default=0)
    goldHandCount = models.IntegerField(u"点金手购买次数", default=0)
    resetElitInstanceCount = models.IntegerField(u"重置精英关卡次数", default=0)
    titanCount = models.IntegerField(u"上古遗迹", default=0) #上古遗迹
    timeGateCount = models.IntegerField(u"元素之塔", default=0)#元素之塔
    giftBagNameId = models.CharField(u"礼包名ID", default="", max_length=200)
    giftBagDiamond = models.IntegerField(u"礼包价格", default=0)
    giftRewards_int = models.CharField(u"奖励", default="", max_length=200)
    descriptionId = models.CharField(u"描述Id", default="", max_length=200)
    growthFund = models.IntegerField(u"能否购买成长基金", default=0)
    resetPVPCount = models.IntegerField(u"竞技场重置次数", default=0)
    dailyRewards_str = models.CharField(u"每日登陆奖励", default="", max_length=200)#rewards 新结构
    statueCount = models.IntegerField(u"可建造的神像总数", default=0)
    plantCount = models.IntegerField(u"可建造的植物总数", default=0)
    #----------攻城战相关----------
    safeTime = models.IntegerField(u"保护时间", default=0)
    fortTime = models.IntegerField(u"堡垒CD", default=0)
    transitTime = models.IntegerField(u"运输时间", default=0) # 资源运输的时间
    resetCost = models.IntegerField(u"冷却堡垒消耗", default=0) # 消除移动堡垒冷却CD的钻石数量
    fortCount = models.IntegerField(u"堡垒数量", default=0)
    transitCount = models.IntegerField(u"运输数量", default=0) # 运输车的数量

    def __unicode(self):
        return "VIP Level:%s" % self.pk
    
    @memoized_property
    def giftRewards(self):
        return [VipReward.get(pk) for pk in self.giftRewards_int.strip().split(",") if pk]

    @memoized_property
    def dailyRewards(self):
        return [get_commonreward(rewardIdStr) for rewardIdStr in self.dailyRewards_str.strip().split(",") if rewardIdStr]

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = self.pk - 1
        dicts["giftRewards"] = [_reward.to_dict() for _reward in self.giftRewards]
        del dicts["id"]
        return dicts

class VipReward(RewardsBase):
    SHEET_NAME = u"VIP礼包"
