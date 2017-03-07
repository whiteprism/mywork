# -*- coding: utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler
from rewards.models import RewardsBase
from common.decorators.memoized_property import memoized_property
from module.common.static import Static
from module.instance.api import get_triggerinfo
from rewards.api import get_commonreward

class Guild(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"公会表"
    level = models.IntegerField(u"公会等级", default=0)
    unlockFunction_int = models.CharField(u"开放功能", default="", max_length=200)
    viceChairmanCount = models.IntegerField(u"副会长个数", default=0)
    memberCount = models.IntegerField(u"公会成员个数", default=0)
    xp = models.IntegerField(u"需要经验", default=0)
    speedCount = models.IntegerField(u"加速次数", default=0)
    beSpeededCount = models.IntegerField(u"被加速次数", default=0)
    levelUpCost = models.IntegerField(u"升级需要花费钻石", default=0)
    chairmanBouns = models.IntegerField(u"会长返利", default=0)
    vichairmanBonus = models.IntegerField(u"副会长返利", default=0)
    memberBouns = models.IntegerField(u"成员返利", default=0)
    speedRewards_int = models.CharField(u"玩家之间加速怎送道具", default="", max_length=200)

    @memoized_property
    def unlockFunction(self):
        if self.unlockFunction_int.strip():
            return [int(pk) for pk in self.unlockFunction_int.strip().split(",") if pk]
        return []
 
    @memoized_property
    def speedRewards(self):
        rewards = []
        rewards_info = [int(float(i)) for i in self.speedRewards_int.strip().split(",") if i]
        reward_counts = rewards_info[0::2]
        reward_ids = rewards_info[1::2]

        for i in range(0, len(reward_ids)):
            rewards.append({"type": reward_ids[i], "count": reward_counts[i]})

        return rewards

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["unlockFunction"] = self.unlockFunction
        dicts["pk"] = self.id
        del dicts["speedRewards"]
        del dicts["id"]
        return dicts

class GuildShop(models.Model, StaticDataRedisHandler, CommonStaticModels):
    _CACHE_FKS = ["show_id"]
    SHEET_NAME = u"公会商店表"
    name = models.CharField(u"名字", max_length=50)
    itemId = models.IntegerField(u"gid",default=0)
    count = models.IntegerField(u"count",default=0)
    cost = models.IntegerField(u"消耗",default=0)
    category = models.IntegerField(u"分类",default=0)
    show_id = models.IntegerField(u"排序",default=0)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()

        dicts["gid"] = dicts["id"]
        del dicts["id"]
        del dicts["name"]
        del dicts["category"]
        del dicts["show_id"]

        return dicts

    @property
    def is_equipfragment(self):
        return self.category == 23

    @property
    def is_item(self):
        return self.category == 26

    @property
    def is_soul(self):
        return self.category == 20

    @property
    def is_artifactfragment(self):
        return self.category == 24

    @classmethod
    def normal_show_ids(cls):
        return [(1, 1), (2,1), (3,1), (4,1), (5, 1), (6,1), (7,1), (8,1)]


    @classmethod
    def get_items_by_show_id(cls, show_id):
        _cache_data = cls.get_list_by_foreignkey("show_id")
        return _cache_data[str(show_id)] if str(show_id) in _cache_data else {}

class GuildFireLevel(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"公会火堆等级"
    xp = models.IntegerField(u"火堆等级所需经验", default=0)

    def to_dict(self):
        # dicts = super(self.__class__, self).to_dict()
        dicts = {}
        dicts["level"] = self.pk
        dicts["xp"] = self.xp
        return dicts

class GuildFireBuff(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"公会火堆BUFF"
    buffName = models.CharField(u"buff名字", default="", max_length=50)
    fireIndex_int = models.CharField(u"BUFF可以存在的火堆INDEX", default="", max_length=50)

    @memoized_property
    def fireIndex(self):
        if self.fireIndex_int.strip():
            return [int(float(i)) for i in self.fireIndex_int.strip().split(",") if i]
        return []

    def get_bufflevel(self, fireLevel, buffLevel):
        return self.buffLevels[fireLevel-1][buffLevel-1]

    @memoized_property
    def buffLevels(self):
        buffLevels = []
        guildFireBuffLevels = GuildFireBuffLevel.get_guild_firebuff_levels_by_fireType(self.pk)

        for guildFireBuffLevel in guildFireBuffLevels:
            if guildFireBuffLevel.fireLevel  > len(buffLevels):
                buffLevels.append([])

            buffLevels[guildFireBuffLevel.fireLevel-1].append(guildFireBuffLevel)

        return buffLevels


    def to_dict(self):
        # dicts = super(self.__class__, self).to_dict()
        dicts = {}
        dicts["pk"] = self.pk
        dicts["fireLevels"] = []
        dicts["buffName"] = self.buffName
        dicts["fireIndex"] = self.fireIndex
        guildFireBuffLevels = GuildFireBuffLevel.get_guild_firebuff_levels_by_fireType(self.pk)

        for guildFireBuffLevel in guildFireBuffLevels:
            if guildFireBuffLevel.fireLevel  > len(dicts["fireLevels"]):
                dicts["fireLevels"].append([])

            dicts["fireLevels"][guildFireBuffLevel.fireLevel-1].append(guildFireBuffLevel.to_dict())

        return dicts

class GuildAuctionReward(models.Model, StaticDataRedisHandler, CommonStaticModels):
    """
    拍卖物品信息
    """
    SHEET_NAME = u"公会拍卖物品"
    basePrice = models.IntegerField(u"起步价格", default=0)
    stepPrice = models.IntegerField(u"价格步长", default=0)
    maxPrice = models.IntegerField(u"价格步长", default=0)
    rewardId = models.CharField("rewardId string", max_length=50)

    @memoized_property
    def reward(self):
        from rewards.api import get_commonreward
        return get_commonreward(self.rewardId)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()

        dicts["pk"] = dicts["id"]
        del dicts["id"]
        return dicts

class GuildFireBuffLevel(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"公会火堆BUFF等级"
    _CACHE_FKS = ["buffType"]
    fireLevel = models.IntegerField(u"火堆等级", default=0)
    buffType = models.IntegerField(u"buff类型",default=0)
    buffValue = models.FloatField(u"buff值",default=0)
    buffLevel = models.IntegerField(u"buff等级",default=0)
    woodCost = models.IntegerField(u"消耗木头",default=0)

    @classmethod
    def get_guild_firebuff_levels_by_fireType(cls, buffType):
        _cache_data = cls.get_list_by_foreignkey("buffType")
        buffLevels =  _cache_data[str(buffType)] if str(buffType) in _cache_data else {}
        buffLevels.sort(lambda x,y: cmp(x.fireLevel,y.fireLevel))
        buffLevels.sort(lambda x,y: cmp(x.buffLevel,y.buffLevel))
        return buffLevels

    def to_dict(self):
        dicts = {}
        dicts["buffValue"] = self.buffValue
        dicts["woodCost"] = self.woodCost
        dicts["fireLevel"] = self.fireLevel
        dicts["buffLevel"] = self.buffLevel

        return dicts

class GuildSiegeBattleReward(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"公会战奖励"
    rewardIds1_str = models.CharField("rewardId string level 1", max_length=100)
    rewardIds2_str = models.CharField("rewardId string level 2", max_length=100)
    rewardIds3_str = models.CharField("rewardId string level 3", max_length=100)
    rewardIds4_str = models.CharField("rewardId string level 4", max_length=100)
    rewardIds5_str = models.CharField("rewardId string level 5", max_length=100)
    rewardIds6_str = models.CharField("rewardId string level 6", max_length=100)
    rewardIds7_str = models.CharField("rewardId string level 7", max_length=100)
    rewardIds8_str = models.CharField("rewardId string level 8", max_length=100)
    rewardIds9_str = models.CharField("rewardId string level 9", max_length=100)
    rewardIds10_str = models.CharField("rewardId string level 10", max_length=100)

    @property
    def rewards_level_1(self):
        return [get_commonreward(reward) for reward in self.rewardIds1_str.strip().split(",") if reward]

    @property
    def rewards_level_2(self):
        return [get_commonreward(reward) for reward in self.rewardIds2_str.strip().split(",") if reward]

    @property
    def rewards_level_3(self):
        return [get_commonreward(reward) for reward in self.rewardIds3_str.strip().split(",") if reward]

    @property
    def rewards_level_4(self):
        return [get_commonreward(reward) for reward in self.rewardIds4_str.strip().split(",") if reward]

    @property
    def rewards_level_5(self):
        return [get_commonreward(reward) for reward in self.rewardIds5_str.strip().split(",") if reward]

    @property
    def rewards_level_6(self):
        return [get_commonreward(reward) for reward in self.rewardIds6_str.strip().split(",") if reward]

    @property
    def rewards_level_7(self):
        return [get_commonreward(reward) for reward in self.rewardIds7_str.strip().split(",") if reward]

    @property
    def rewards_level_8(self):
        return [get_commonreward(reward) for reward in self.rewardIds8_str.strip().split(",") if reward]

    @property
    def rewards_level_9(self):
        return [get_commonreward(reward) for reward in self.rewardIds9_str.strip().split(",") if reward]

    @property
    def rewards_level_10(self):
        return [get_commonreward(reward) for reward in self.rewardIds10_str.strip().split(",") if reward]
   
    def get_reward_by_level(self, level):
        '''
            根据公会等级获取相应的奖励
        '''
        rewards = []
        if level == 1:
            rewards = self.rewards_level_1

        elif level == 2:
            rewards = self.rewards_level_2

        elif level == 3:
            rewards = self.rewards_level_3

        elif level == 4:
            rewards = self.rewards_level_4

        elif level == 5:
            rewards = self.rewards_level_5

        elif level == 6:
            rewards = self.rewards_level_6

        elif level == 7:
            rewards = self.rewards_level_7

        elif level == 8:
            rewards = self.rewards_level_8

        elif level == 9:
            rewards = self.rewards_level_9

        elif level == 10:
            rewards = self.rewards_level_10

        return rewards

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        return dicts
