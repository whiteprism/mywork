# -*- coding: utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
#from common.models import CommonStaticUnitModels, CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler
#from rewards.api import get_hero_eveolve_cost
from rewards.models import RewardsBase
from rewards.api import get_commonreward
from module.common.static import Static
from common.decorators.memoized_property import memoized_property
import datetime
from module.hero.api import get_card,get_warrior_by_upgrade,get_herostar
from module.equip.api import get_cardequip
from django.conf import settings
import random

class Instance(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"章节"
    
    name = models.CharField(u"章节名称", max_length=200)
    rewardIds_1_int = models.CharField(u"Reward_int", max_length=200, default="")
    rewardCounts_1_int = models.CharField(u"count_int", max_length=200, default="")
    rewardIds_2_int = models.CharField(u"Reward_int", max_length=200, default="")
    rewardCounts_2_int = models.CharField(u"count_int", max_length=200, default="")
    rewardIds_3_int = models.CharField(u"Reward_int", max_length=200, default="")
    rewardCounts_3_int = models.CharField(u"count_int", max_length=200, default="")
    eliteRewardIds_1_int = models.CharField(u"Reward_int", max_length=200, default="")
    eliteRewardCounts_1_int = models.CharField(u"count_int", max_length=200, default="")
    eliteRewardIds_2_int = models.CharField(u"Reward_int", max_length=200, default="")
    eliteRewardCounts_2_int = models.CharField(u"count_int", max_length=200, default="")
    eliteRewardIds_3_int = models.CharField(u"Reward_int", max_length=200, default="")
    eliteRewardCounts_3_int = models.CharField(u"count_int", max_length=200, default="")
    rewardsId_int = models.CharField(u"奖励_int", max_length=1000, default="")
    counts_int = models.CharField(u"奖励_counts", max_length=200, default="")
    probability =  models.FloatField(u"概率", default=0)

    def __unicode__(self):
        return u"%s:%s" %(self.pk, self.name)

    class Meta:
        ordering = ["id"]

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        hasLevel0 = False
        hasLevel1 = False
        hasLevel2 = False
        hasEliteLevel0 = False
        hasEliteLevel1 = False
        hasEliteLevel2 = False
        if self.boxData[0]:
            hasLevel0 = True
        if self.boxData[1]:
            hasLevel1 = True
        if self.boxData[2]:
            hasLevel2 = True
        if self.eliteBoxData[0]:
            hasEliteLevel0 = True
        if self.eliteBoxData[1]:
            hasEliteLevel1 = True
        if self.eliteBoxData[2]:
            hasEliteLevel2 = True
        dicts["level0Reward"] = self.boxData[0]
        dicts["level1Reward"] = self.boxData[1]
        dicts["level2Reward"] = self.boxData[2]

        dicts["hasLevel0"] = hasLevel0
        dicts["hasLevel1"] = hasLevel1
        dicts["hasLevel2"] = hasLevel2

        dicts["level0EliteReward"] = self.eliteBoxData[0]
        dicts["level1EliteReward"] = self.eliteBoxData[1]
        dicts["level2EliteReward"] = self.eliteBoxData[2]

        dicts["hasEliteLevel0"] = hasEliteLevel0
        dicts["hasEliteLevel1"] = hasEliteLevel1
        dicts["hasEliteLevel2"] = hasEliteLevel2

        dicts["pk"] = self.id


        del dicts["id"]
        del dicts["name"]
        del dicts["rewardIds_1"]
        del dicts["rewardIds_2"]
        del dicts["rewardIds_3"]
        del dicts["rewardCounts_1"]
        del dicts["rewardCounts_2"]
        del dicts["rewardCounts_3"]
        del dicts["eliteRewardIds_1"]
        del dicts["eliteRewardIds_2"]
        del dicts["eliteRewardIds_3"]
        del dicts["eliteRewardCounts_1"]
        del dicts["eliteRewardCounts_2"]
        del dicts["eliteRewardCounts_3"]
        return dicts

    @memoized_property
    def boxData(self):
        box_list = []
        #box 1
        type_list1 = [int(float(i)) for i in self.rewardIds_1_int.strip().split(",") if i]
        count_list1 = [int(float(c)) for c in self.rewardCounts_1_int.strip().split(",") if c]
        temp_list1 = []
        for index in range(0,len(type_list1)): 
            data = {}
            data["type"] = type_list1[index]
            data["count"] = count_list1[index]
            temp_list1.append(data)
        box_list.append(temp_list1)
        #box 2
        temp_list2 = []
        type_list2 = [int(float(i)) for i in self.rewardIds_2_int.strip().split(",") if i]
        count_list2 = [int(float(c)) for c in self.rewardCounts_2_int.strip().split(",") if c]
        for index in range(0,len(type_list2)): 
            data = {}
            data["type"] = type_list2[index]
            data["count"] = count_list2[index]
            temp_list2.append(data)
        box_list.append(temp_list2)
        #box 3
        temp_list3 = []
        type_list3 = [int(float(i)) for i in self.rewardIds_3_int.strip().split(",") if i]
        count_list3 = [int(float(c)) for c in self.rewardCounts_3_int.strip().split(",") if c]
        for index in range(0,len(type_list3)): 
            data = {}
            data["type"] = type_list3[index]
            data["count"] = count_list3[index]
            temp_list3.append(data)
        box_list.append(temp_list3)

        return box_list

    @memoized_property
    def eliteBoxData(self):
        box_list = []
        #box 1
        type_list1 = [int(float(i)) for i in self.eliteRewardIds_1_int.strip().split(",") if i]
        count_list1 = [int(float(c)) for c in self.eliteRewardCounts_1_int.strip().split(",") if c]
        temp_list1 = []
        for index in range(0,len(type_list1)): 
            data = {}
            data["type"] = type_list1[index]
            data["count"] = count_list1[index]
            temp_list1.append(data)
        box_list.append(temp_list1)
        #box 2
        temp_list2 = []
        type_list2 = [int(float(i)) for i in self.eliteRewardIds_2_int.strip().split(",") if i]
        count_list2 = [int(float(c)) for c in self.eliteRewardCounts_2_int.strip().split(",") if c]
        for index in range(0,len(type_list2)): 
            data = {}
            data["type"] = type_list2[index]
            data["count"] = count_list2[index]
            temp_list2.append(data)
        box_list.append(temp_list2)
        #box 3
        temp_list3 = []
        type_list3 = [int(float(i)) for i in self.eliteRewardIds_3_int.strip().split(",") if i]
        count_list3 = [int(float(c)) for c in self.eliteRewardCounts_3_int.strip().split(",") if c]
        for index in range(0,len(type_list3)): 
            data = {}
            data["type"] = type_list3[index]
            data["count"] = count_list3[index]
            temp_list3.append(data)
        box_list.append(temp_list3)

        return box_list

    @memoized_property
    def rewardData(self):
        '''
        章节奖励结构
        '''
        data = {}
        data["type"] = [int(float(i)) for i in self.rewardsId_int.strip().split(",") if i]
        data["count"] = [int(float(c)) for c in self.counts_int.strip().split(",") if c]
        data["probability"] = self.probability
        return data


class InstanceLevel(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"关卡"
    _CACHE_FKS = ["instance_id"]
    name = models.CharField(u"关卡名称", max_length=200, default="")
    descriptionId = models.CharField(u"关卡描述", max_length=200, default="")
    instance_id = models.IntegerField(u"篇章ID")
    maxPlayCount = models.IntegerField(u"最大挑战次数", default=0)
    monsterId = models.IntegerField(u"BOSSid",  default=0)
    nameId = models.CharField(u"名字id", max_length = 30, default="")
    playerExp = models.IntegerField(u"玩家经验", default=0)
    scene = models.CharField(u"场景名字", max_length=60, default="")
    powerCost = models.IntegerField(u"消耗体力", default=0)
    levelIndex = models.IntegerField(u"关卡位置index", default=0)
    minUserLevel = models.IntegerField(u"最小解锁等级", default=0)
    nextInstanceId = models.IntegerField(u'下一关卡id', default = 0)
    heroExp_int = models.CharField(u"各难度英雄经验", max_length=100, default="")
    golds_int = models.CharField(u"各难度掉落的金钱", max_length=100, default="")
    woods_int = models.CharField(u"各难度掉落的木头", max_length=100, default="")
    revisionScale_float = models.CharField(u"revisionScale_float", max_length=100, default="")
    rewardId_int = models.CharField(u"InstanceReward_int", max_length=200, default="")
    probability_float = models.CharField(u'掉落概率', max_length = 100, default="")
    count_int = models.CharField(u"对应数量", max_length=100, default="")
    mustRewardId_int = models.CharField(u"一定掉落的id", max_length=100, default="")
    enemyIds_int =  models.CharField(u"敌人的id", max_length=100, default="")
    zoneIDs_int = models.CharField(u"关卡使用的场景区域", max_length=1000, default="")
    triggerInfos_int = models.CharField(u"触发器", max_length=500, default="")
    instanceStartDialogID = models.IntegerField(default=0)
    instanceEndDialogID = models.IntegerField(default=0)

    def __getattribute__(self, name):
        if name == 'instance':
            return self._related_instance
        return object.__getattribute__(self, name)

    @memoized_property
    def golds(self):
        return [int(float(gold)) for gold in self.golds_int.strip().split(",") if gold]

    @memoized_property
    def woods(self):
        return [int(float(wood)) for wood in self.woods_int.strip().split(",") if wood]

    @memoized_property
    def enemyIds(self):
        return [int(float(enemyId)) for enemyId in self.enemyIds_int.strip().split(",") if enemyId]

    @memoized_property
    def enemies(self):
        return [Enemy.get(enemyId) for enemyId in self.enemyIds]


    @memoized_property
    def heroExp(self):
        return [int(float(heroExp)) for heroExp in self.heroExp_int.strip().split(",") if heroExp]
    
    @memoized_property
    def _related_instance(self):
        return Instance.get(self.instance_id)

    @memoized_property
    def instanceReward(self):
        '''
        副本奖励静态展示数据
        '''
        data = []
        data_type = [i for i in self.rewardId_int.strip().split(",") if i]
        data_count = [c for c in self.count_int.strip().split(",") if c]
        for i in range(0, len(data_type)):
            dic = {}
            dic["type"] = int(float(data_type[i]))
            dic["count"] = int(float(data_count[i]))
            data.append(dic)
        return data

    @memoized_property
    def rewardData(self):
        '''
        掉落奖励数据
        '''
        data = {}
        p_list = []
        p_list = self.probability_float.strip().split(",")
        data["type"] = [int(float(i)) for i in self.rewardId_int.strip().split(",") if i]
        data["count"] = [int(float(c)) for c in self.count_int.strip().split(",") if c]
        data["probability"] = [float(p) for p in p_list if p]
        data["mustId"] = [int(float(mi)) for mi in self.mustRewardId_int.strip().split(",") if mi]
        return data



    @memoized_property
    def triggerInfos(self):
        if self.triggerInfos_int.strip():
            return [TriggerInfo.get(int(float(pk))) for pk in self.triggerInfos_int.strip().split(",") if pk]
        return []


    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["InstanceReward"] = self.instanceReward
        dicts["levelId"] = dicts["id"]
        dicts["instanceId"] = dicts["instance_id"]
        dicts["triggerInfos"] = [triggerInfo.to_dict() for triggerInfo in self.triggerInfos]

        enemy = None
        if self.enemyIds:
            enemy = []
            for singleenemyid in self.enemyIds:
                if not Enemy.get(singleenemyid):
                    print singleenemyid,u"这个id *******在这个字段数据里面-->",self.enemyIds, u"属于这个副本-->", self.id
                enemy.append(Enemy.get(singleenemyid))

        hero_list = []
        warrior_list = []
        if enemy:
            for singleenemy in enemy:
                for i in singleenemy.warriorIds:
                    if i:
                        if int(str(int(float(i)))[0:2]) == 11 and int(float(i)) not in hero_list:
                            hero_list.append(int(float(i)))
                            hero_list.append(singleenemy.heroLevel)
                            hero_list.append(singleenemy.heroStar)
                            hero_list.append(singleenemy.heroUp)

                        else:
                            if not int(float(i)) in warrior_list:
                                warrior_list.append(int(float(i)))
                                warrior_list.append(singleenemy.soldierLevel)
                                warrior_list.append(singleenemy.heroStar)
                                warrior_list.append(singleenemy.heroUp)

        dicts["heroIds"] = (hero_list + warrior_list)

        del dicts["nextInstanceId"]
        return dicts
    
    @classmethod
    def get_instancelevel_by_instance_id(cls, instance_id):
        _cache_data = cls.get_list_by_foreignkey("instance_id")
        return _cache_data[str(instance_id)] if str(instance_id) in _cache_data else {}


class GuildInstanceLevel(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"公会关卡"

    name = models.CharField(u"关卡名称", max_length=200, default="")
    descriptionId = models.CharField(u"关卡描述", max_length=200, default="")
    monsterId = models.IntegerField(u"BOSSid",  default=0)
    nameId = models.CharField(u"名字id", max_length = 30, default="")
    scene = models.CharField(u"场景名字", max_length=60, default="")
    levelIndex = models.IntegerField(u"关卡位置index", default=0)

    revisionScale_float = models.CharField(u"revisionScale_float", max_length=100, default="")
    probability_float = models.CharField(u'掉落概率', max_length = 100, default="")   
    aucRewardIds_int = models.CharField(u"InstanceReward_int", max_length=200, default="")
    aucRewardMaxCount_int = models.CharField(u'掉落物品数量', max_length = 100, default="")
    diamondCost = models.IntegerField(u"消耗钻石", default=0)
    enemyIds_int =  models.CharField(u"敌人的id", max_length=100, default="")
    zoneIDs_int = models.CharField(u"关卡使用的场景区域", max_length=1000, default="")
    triggerInfos_int = models.CharField(u"触发器", max_length=500, default="")
    guildLevelLimit = models.IntegerField(u"开启副本等级",  default=0)
    rewardGold = models.IntegerField(u"该副本奖励的总公会币", default=0)

    @memoized_property
    def enemyIds(self):
        return [int(float(enemyId)) for enemyId in self.enemyIds_int.strip().split(",") if enemyId]

    @memoized_property
    def enemies(self):
        return [Enemy.get(enemyId) for enemyId in self.enemyIds]


    @memoized_property
    def bossHp(self):
        enemies = self.enemies
        hp = 0
        for enemy in enemies:
            warriorIds = enemy.warriorIds
            for warriorId in warriorIds:
                warrior = get_warrior_by_upgrade(warriorId, enemy.heroUp)
                heroStar = get_herostar(warrior.cardId, enemy.heroStar)
                hp += (warrior.hero.hp + heroStar.hpGrow * 1.0 * (enemy.heroLevel - 1)) * (1 + heroStar.growPercent) * enemy.propertyValues[0]
        #print p_list
        return int(hp) 


    @memoized_property
    def heroExp(self):
        return [int(float(heroExp)) for heroExp in self.heroExp_int.strip().split(",") if heroExp]

    # @memoized_property
    # def instanceReward(self):
    #     '''
    #     副本奖励静态展示数据
    #     '''
    #     data = []
    #     data_type = [i for i in self.rewardId_int.strip().split(",") if i]
    #     data_count = [c for c in self.count_int.strip().split(",") if c]
    #     data_price = [p for p in self.price_int.strip().split(",") if p]

    #     for i in range(0, len(data_type)):
    #         dic = {}
    #         dic["type"] = int(float(data_type[i]))
    #         dic["count"] = int(float(data_count[i]))
    #         dic["level"] = int(float(data_price[i]))
    #         data.append(dic)
    #     return data

    @memoized_property
    def rewardData(self):
        '''
        掉落奖励数据
        '''
        data = {}
        data["aucRewardIds"] = [int(float(i)) for i in self.aucRewardIds_int.strip().split(",") if i]
        data["aucRewardMaxCount"] = [int(float(p)) for p in self.aucRewardMaxCount_int.strip().split(",") if p]
        data["probability"] = [float(p) for p in self.probability_float.strip().split(",") if p]
        return data

    @memoized_property
    def triggerInfos(self):
        if self.triggerInfos_int.strip():
            return [TriggerInfo.get(int(float(pk))) for pk in self.triggerInfos_int.strip().split(",") if pk]
        return []


    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["levelId"] = dicts["id"]
        dicts["triggerInfos"] = [triggerInfo.to_dict() for triggerInfo in self.triggerInfos]

        enemy = None
        if self.enemyIds:
            enemy = []
            for singleenemyid in self.enemyIds:
                enemy.append(Enemy.get(singleenemyid))
                if not Enemy.get(singleenemyid):
                    print singleenemyid, u"这个id这敌军阵容表里面没有"

        hero_list = []
        warrior_list = []
        if enemy:
            for singleenemy in enemy:
                for i in singleenemy.warriorIds:
                    if i:
                        if int(str(int(float(i)))[0:2]) == 11 and int(float(i)) not in hero_list:
                            hero_list.append(int(float(i)))
                            hero_list.append(singleenemy.heroLevel)
                            hero_list.append(singleenemy.heroStar)
                            hero_list.append(singleenemy.heroUp)

                        else:
                            if not int(float(i)) in warrior_list:
                                warrior_list.append(int(float(i)))
                                warrior_list.append(singleenemy.soldierLevel)
                                warrior_list.append(singleenemy.heroStar)
                                warrior_list.append(singleenemy.heroUp)

        dicts["heroIds"] = (hero_list + warrior_list)

        return dicts

class EliteInstanceLevel(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"精英关卡"
    _CACHE_FKS = ["instance_id"]
    name = models.CharField(u"关卡名称", max_length=200, default="")
    descriptionId = models.CharField(u"关卡描述", max_length=200, default="")
    instance_id = models.IntegerField(u"篇章ID")
    eliteMaxPlayCount = models.IntegerField(u"精英最大挑战次数", default=0)
    monsterId = models.IntegerField(u"BOSSid",  default=0)
    nameId = models.CharField(u"名字id", max_length = 30, default="")
    scene = models.CharField(u"场景名字", max_length=60, default="")
    elitePowerCost = models.IntegerField(u"精英消耗体力", default=0)
    levelIndex = models.IntegerField(u"关卡位置index", default=0)
    eliteMinUserLevel = models.IntegerField(u"最小解锁等级", default=0)
    eliteHeroExp = models.IntegerField(u"英雄经验", default=0)
    eliteRevisionScale = models.FloatField(u"难度系数", default=0)
    eliteNextInstanceId = models.IntegerField(u'下一精英关卡的id', default = 0)
    eliteGold = models.IntegerField(u"金钱", default=0)
    elitewoods_int = models.CharField(u"精英各难度掉落的木头", max_length=100, default="")
    elitePlayerExp = models.IntegerField(u"精英玩家经验", default=0)
    eliteRewardId_int = models.CharField(u"InstanceReward_int", max_length=200, default="")
    eliteProbability_float = models.CharField(u'掉落概率', max_length = 100, default="")
    eliteCount_int = models.CharField(u"对应数量", max_length=100, default="")
    mustEliteRewardId_int = models.CharField(u"一定掉落的id", max_length=100, default="")
    eliteEnemyIds_int = models.CharField(u"精英敌方阵容", max_length=500, default="")
    zoneIDs_int = models.CharField(u"关卡使用的场景区域", max_length=1000, default="")
    triggerInfos_int = models.CharField(u"触发器", max_length=500, default="")

    def __getattribute__(self, name):
        if name == 'instance':
            return self._related_instance
        return object.__getattribute__(self, name)

    @memoized_property
    def elitewoods(self):
        return [int(float(elitewoods)) for elitewoods in self.elitewoods_int.strip().split(",") if elitewoods]

    @memoized_property
    def eliteEnemyIds(self):
        return [int(float(enemyId)) for enemyId in self.eliteEnemyIds_int.strip().split(",") if enemyId]
    @memoized_property
    def eliteEnemies(self):
        return [Enemy.get(eliteEnemyId) for eliteEnemyId in self.eliteEnemyIds]


    @memoized_property
    def _related_instance(self):
        return Instance.get(self.instance_id)


    @memoized_property
    def eliteInstanceReward(self):
        '''
        副本奖励静态展示数据
        '''
        data = []
        data_type = [i for i in self.eliteRewardId_int.strip().split(",") if i]
        data_count = [c for c in self.eliteCount_int.strip().split(",") if c]
        for i in range(0, len(data_type)):
            dic = {}
            dic["type"] = int(float(data_type[i]))
            dic["count"] = int(float(data_count[i]))
            data.append(dic)
        return data

    @memoized_property
    def eliteRewardData(self):
        '''
        掉落奖励数据
        '''
        data = {}
        data["type"] = [int(float(i)) for i in self.eliteRewardId_int.strip().split(",") if i]
        data["count"] = [int(float(c)) for c in self.eliteCount_int.strip().split(",") if c]
        data["probability"] = [float(p) for p in self.eliteProbability_float.strip().split(",") if p]
        data["mustId"] = [int(float(mi)) for mi in self.mustEliteRewardId_int.strip().split(",") if mi]
        return data

    @memoized_property
    def triggerInfos(self):
        if self.triggerInfos_int.strip():
            return [TriggerInfo.get(int(float(pk))) for pk in self.triggerInfos_int.strip().split(",") if pk]
        return []


    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["eliteInstanceReward"] = self.eliteInstanceReward
        dicts["levelId"] = dicts["id"]
        dicts["instanceId"] = dicts["instance_id"]
        dicts["triggerInfos"] = [triggerInfo.to_dict() for triggerInfo in self.triggerInfos]


        eliteEnemy = None

        if self.eliteEnemyIds:
            eliteEnemy = []
            for singleeliteenemyid in self.eliteEnemyIds:
                if not Enemy.get(singleeliteenemyid):
                    print u"这个ｉｄ", singleeliteenemyid,u"在这个精英关卡中",self.id
                eliteEnemy.append(Enemy.get(singleeliteenemyid))



        e_hero_list = []
        e_warrior_list = []
        if eliteEnemy:
            for singleeliteenemy in eliteEnemy:
                for i in singleeliteenemy.warriorIds:
                    if i:
                        if int(str(int(float(i)))[0:2]) == 11 and int(float(i)) not in e_hero_list:
                            e_hero_list.append(int(float(i)))
                            e_hero_list.append(singleeliteenemy.heroLevel)
                            e_hero_list.append(singleeliteenemy.heroStar)
                            e_hero_list.append(singleeliteenemy.heroUp)
                        else:
                            if not int(float(i)) in e_warrior_list:
                                e_warrior_list.append(int(float(i)))
                                e_warrior_list.append(singleeliteenemy.soldierLevel)
                                e_warrior_list.append(singleeliteenemy.heroStar)
                                e_warrior_list.append(singleeliteenemy.heroUp)

        dicts["eliteHeroIds"] = e_hero_list + e_warrior_list
        del dicts["eliteNextInstanceId"]
        return dicts

    @classmethod
    def get_eliteinstancelevel_by_instance_id(cls, eliteinstance_id):
        _cache_data = cls.get_list_by_foreignkey("instance_id")
        return _cache_data[str(eliteinstance_id)] if str(eliteinstance_id) in _cache_data else {}

class Raid(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"活动副本"
    descriptionId = models.CharField(u"关卡描述", max_length=200, default="")
    easyTextId = models.CharField(u"id", max_length=200, default="")
    heroId = models.CharField(u"英雄id", max_length = 30, default=0)
    nameId = models.CharField(u"名字id", max_length = 30, default="")
    normalTextId = models.CharField(u"文字id", max_length = 30, default="")
    openTimeTextId = models.CharField(u"文字id", max_length = 30, default="")
    powerCost = models.IntegerField(u"体力消耗", default=0)
    textId = models.CharField(u"文字id", max_length = 30, default="")
    category = models.IntegerField(u"类型", default=0)
    raidLevelId_int = models.CharField(u"活动下包含的难度等级", max_length=200, default="")
    vocationType = models.IntegerField(u"职业限制", default = 0)
    maxPlayCount = models.IntegerField(u"最大挑战次数", default=0)
    experiment1 = models.CharField(u"实验1, 开启日期", max_length=200, default = '')
    experiment2 = models.CharField(u"实验2, 双倍", max_length=200, default = '')


    @memoized_property
    def raidLevels(self):
        '''
        所有难度
        '''
        data = []
        for raidLevelId in [int(float(l)) for l in self.raidLevelId_int.strip().split(",") if l]:
            data.append(RaidLevelConf.get(raidLevelId))
        return data

    @memoized_property
    def raidLevel_ids(self):
        '''
        所有难度
        '''
        return [int(float(l)) for l in self.raidLevelId_int.strip().split(",") if l]

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = self.id
        dicts["levelConfs"] = [raidLevelConf.to_dict() for raidLevelConf in self.raidLevels if raidLevelConf]
        del dicts["id"]
        return dicts

class RaidLevelConf(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"活动副本关卡"
    nameId = models.CharField(u"名字id", max_length = 30, default="")
    descriptionId = models.CharField(u"关卡描述", max_length=200, default="")
    difficulty = models.IntegerField(u"难度", default=0)
    heroExp = models.IntegerField(u"英雄经验", default=0)
    playerExp = models.IntegerField(u"玩家经验", default=0)
    minUserLevel = models.IntegerField(u"最小解锁等级", default=0)
    maxUserLevel = models.IntegerField(u"最大解锁等级", default=0)
    monsterId = models.IntegerField(u"BOSSid", default=0)
    revisionScale = models.FloatField(u"难度系数", default=0)
    scene = models.CharField(u"场景名字", max_length=60, default="")
    gold = models.IntegerField(u"金币", default=0)
    rewardId_int = models.CharField(u"InstanceReward_int", max_length=2500, default="")
    probability_float = models.CharField(u'掉落概率', max_length = 700, default="")
    count_float = models.CharField(u"对应数量", max_length=700, default="")
    minCount_float = models.CharField(u"对应波动最小数量", max_length=700, default="")
    enemyIds_int = models.CharField(u"敌方阵容", max_length=1000, default="")
    iconId = models.CharField(u"敌方阵容", max_length=20, default="")
    raidLevelName = models.CharField(u"关卡名字", max_length=100, default="")
    zoneIDs_int = models.CharField(u"关卡使用的场景区域", max_length=1000, default="")
    triggerInfos_int = models.CharField(u"触发器", max_length=500, default="")
    backImageId = models.CharField(u"背景ui图片", max_length=20, default="")
    extroImageId = models.CharField(u"额外新背景ui图片", max_length=20, default="")
    suggestHeroIds_int = models.CharField(u"推荐上阵英雄ID", max_length=1000, default="")

    def __getattribute__(self, name):
        return object.__getattribute__(self, name)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["reward"] = self.rewards
        dicts["pk"] = self.id
        dicts["triggerInfos"] = [triggerInfo.to_dict() for triggerInfo in self.triggerInfos]

        return dicts

    @memoized_property
    def triggerInfos(self):
        if self.triggerInfos_int.strip():
            return [TriggerInfo.get(int(float(pk))) for pk in self.triggerInfos_int.strip().split(",") if pk]
        return []

    @memoized_property
    def rewards(self):
        '''
        奖励list
        '''
        temp_list = []
        reward_ids = [int(float(i)) for i in self.rewardId_int.strip().split(",") if i]
        reward_counts = [float(c) for c in self.count_float.strip().split(",") if c]
        # reward_minCounts = [float(c) for c in self.minCount_float.strip().split(",") if c]

        for i in range(0, len(reward_ids)):
            data = {}
            data["type"] = reward_ids[i]
            data["count"] = 0
            # data["minCounts"] = reward_minCounts[i]

            temp_list.append(data)
        return temp_list

    @memoized_property
    def rewardData(self):
        '''
        奖励数据(计算用)
        '''
        data = {}
        data["type"] = [int(float(i)) for i in self.rewardId_int.strip().split(",") if i]
        data["count"] = [float(c) for c in self.count_float.strip().split(",") if c]
        data["minCount"] = [float(c) for c in self.minCount_float.strip().split(",") if c]
        data["probability"] = [float(p)  for p in self.probability_float.strip().split(",") if p]
        return data

    @memoized_property
    def enemyIds(self):
        return [int(float(enemyId)) for enemyId in self.enemyIds_int.strip().split(",") if enemyId]

    @memoized_property
    def enemies(self):
        return [Enemy.get(enemyId) for enemyId in self.enemyIds]

class InstanceReward(RewardsBase):
    SHEET_NAME = u"副本掉落"
    
class Enemy(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"敌军阵容"
    warriorIds_int = models.CharField(u"hero_gid_int", max_length=500, default="")
    posPoints_int = models.CharField(u"站位", max_length=500, default="")
    propertyHeros_int = models.CharField(u"特定属性加成的英雄", max_length=200, default="")
    propertyIds_int = models.CharField(u"特定属性ids", max_length=200, default="")
    skillIds_int = models.CharField(u"增加的 技能id-等级", max_length=200, default="")
    propertyValues_float = models.CharField(u"特定属性数值百分比", max_length=200, default="")
    heroLevel = models.IntegerField(u"英雄等级", default=0)
    heroStar = models.IntegerField(u"英雄星级", default=0)
    heroUp = models.IntegerField(u"英雄加几", default=0)
    soldierLevel = models.IntegerField(u"小兵等级", default=0)
    skillLevel = models.IntegerField(u"技能等级", default=0)
    equipLevel = models.IntegerField(u"装备等级", default=0)
    equipUpgrade = models.IntegerField(u"装备阶级", default=0)
    bubbleTypes_int = models.CharField(u"气泡分类", max_length=500, default="")
    bubbleMessages_str = models.CharField(u"气泡内容", max_length=500, default="")
    bubbleProperbility_float = models.CharField(u"气泡出现概率", max_length=500, default="")

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["soldierLevel"] = dicts["soldierLevel"] - 1
        dicts["skillLevel"] = dicts["skillLevel"] - 1
        dicts["equipInfos"] = self.equipInfos
        dicts["pk"] = self.id
        del dicts["id"]
        return dicts

    @memoized_property
    def warriorIds(self):
        return [int(float(pk)) for pk in self.warriorIds_int.strip().split(",") if pk]
    @memoized_property
    def skillIds(self):
        return [int(float(pk)) for pk in self.skillIds_int.strip().split(",") if pk]
    @memoized_property
    def bubbleTypes(self):
        return [int(float(pk)) for pk in self.bubbleTypes_int.strip().split(",") if pk]
    @memoized_property
    def bubbleMessages(self):
        return [pk for pk in self.bubbleMessages_str.strip().split(",") if pk]
    @memoized_property
    def bubbleProperbility(self):
        return [float(pk) for pk in self.bubbleProperbility_float.strip().split(",") if pk]

    @memoized_property
    def propertyIds(self):
        return [float(pk) for pk in self.propertyIds_int.strip().split(",") if pk]

    @memoized_property
    def propertyValues(self):
         return [float(pk) for pk in self.propertyValues_float.strip().split(",") if pk]

    @memoized_property
    def equip_infos(self):
        infos = []
        for warrior_id in self.warriorIds:
            if int(str(warrior_id)[0:2]) == 11:

                card = get_card(warrior_id)

                if card:
                    equips = get_cardequip(card.career)

                    for i in range(1, 5):
                        if self.equipLevel < 0:
                            infos.append(-1)
                            infos.append(-1)
                        else:
                            pos_equips = getattr(equips, "pos%s" % i)
                            infos.append(pos_equips[self.equipUpgrade])
                            infos.append(self.equipLevel)

        return infos

    @classmethod
    def create_cache_all(cls): 
        enemies = list(cls.objects.all())
        id_to_instance = {}
        for enemy in enemies:
            enemy.equipInfos = enemy.equip_infos
            id_to_instance[enemy.pk] = enemy
        
        if settings.ENABLE_REDIS_CACHE:
            cls.redis_set(cls.get_kvs_key(), id_to_instance)
        cls._id_to_instance = id_to_instance

class Trigger(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"触发器"
    triggerType = models.IntegerField(u"触发器类型", default = 0)
    bOnce = models.IntegerField(u"bOnce", default = 0)
    data_int = models.CharField(u"触发器行为", max_length=500, default="")

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["data"] = [_data.to_dict() for _data in self.data]
        return dicts

    @memoized_property
    def data(self):
        if self.data_int.strip():
            return [TriggerData.get(int(float(pk))) for pk in self.data_int.strip().split(",") if pk]
        return []

class TriggerData(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"触发器行为"
    id = models.BigIntegerField(u"主键",primary_key = True)
    eventType = models.IntegerField(u"事件类型", default= 0)
    delay = models.FloatField(u"延迟", default=0.0)
    param_1 = models.IntegerField(u"参数1", default= 0)
    param_2 = models.IntegerField(u"参数2", default= 0)
    param_3 = models.IntegerField(u"参数3", default= 0)
    param_4 = models.IntegerField(u"参数4", default= 0)
    param_5 = models.IntegerField(u"参数5", default= 0)
    param_6 = models.IntegerField(u"参数6", default= 0)
    param_7 = models.IntegerField(u"参数7", default= 0)
    param_8 = models.IntegerField(u"参数8", default= 0)
    param_9 = models.IntegerField(u"参数9", default= 0)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        del dicts["id"]
        return dicts

class Zone(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"场景区域"
    attackDir = models.IntegerField(u"attackDir", default=0)
    zoneID = models.IntegerField(u"区域编号", default=0)
    startPoints_int = models.CharField(u"startPoints", max_length=200, default="")
    airGatesToActivate_int =  models.CharField(u"airGatesToActivate", max_length=200, default="") 

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        return dicts

class TriggerInfo(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"触发器信息"
    nameID = models.IntegerField(u"nameID", default=0)
    triggerID = models.IntegerField(u"触发器ID", default=0)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        del dicts["id"]
        return dicts

class SmallGame(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"小游戏"
    score = models.IntegerField(u"score", default=0)
    rewards_int = models.CharField(u"smallintreward", max_length=100, default="")

    @memoized_property 
    def rewards(self):
        return [SmallGameReward.get(int(float(pk))) for pk in self.rewards_int.strip().split(",") if pk]
    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["reward"] = self.rewards
        dicts["pk"] = self.id
        return dicts

class SmallGameReward(RewardsBase):
    SHEET_NAME = u"小游戏奖励"

class ElementTowerInstance(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"元素之塔关卡"
    name = models.CharField(u"名字", max_length=50, default="")
    iconId = models.CharField(u"ICON", max_length=50, default="")
    descriptionId = models.CharField(u"描述", max_length=50, default="")
    bgImageId = models.CharField(u"background image ID", max_length=50, default="")
    extroImageId = models.CharField(u"extro image ID", max_length=50, default="")
    difficulty = models.IntegerField(u"难度", default=0)
    minUserLevel = models.IntegerField(u"玩家最小等级", default=0)
    scene = models.CharField(u"场景", max_length=50, default="")
    rewardIds_str = models.CharField(u"奖励ID", max_length=500, default="")
    suggestHeroIds_int = models.CharField(u"推荐阵容", max_length=300, default="")

    @memoized_property
    def levels(self):
        levels = ElementTowerLevel.get_instancelevel_by_tower_id(self.pk)
        levels.sort(lambda x,y: x.level > y.level)
        return levels


    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = self.id
        del dicts["id"]
        levels = self.levels
        dicts["levels"] = [level.to_dict() for level in levels]

        return dicts

class ElementTowerBuff(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"元素之塔BUFF"
    attrTypes_str = models.CharField(u"属性s", max_length=300, default="")
    extras_float = models.CharField(u"属性加成", max_length=300, default="")
    iconId = models.CharField(u"ICON", max_length=50, default="")

    @memoized_property
    def attrs(self):
        """
        buff 属性
        """
        attrTypes = [str(attrType) for attrType in self.attrTypes_str.strip().split(",") if attrType]
        extras = [float(extra) for extra in self.extras_float.strip().split(",") if extra]

        attrs = []
        for attrType in attrTypes:
            attrs.append((attrType, extras))
        return attrs

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = self.id
        del dicts["id"]
        return dicts

class ElementTowerLevel(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"元素之塔关卡掉落"
    _CACHE_FKS = ["towerId"]
    monsterId = models.IntegerField(u"怪物", default=0)
    towerId = models.IntegerField(u"塔ID", default=0)
    level = models.IntegerField(u"层级", default=0)
    nameId = models.CharField(u"名字id", max_length=200, default="")
    rewardIds_str = models.CharField(u"奖励", max_length=300, default="")
    difficulties_float = models.CharField(u"难度", max_length=300, default="")
    diamondRewardIds_str = models.CharField(u"钻石开宝箱", max_length=300, default="")
    diamondCosts_int = models.CharField(u"钻石开宝箱消耗", max_length=300, default="")
    enemyId = models.IntegerField(u"敌军阵容ID", default=0)
    zoneIDs_int = models.CharField(u"zone ID", max_length=300, default="")
    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = self.id
        del dicts["id"]
        return dicts

    @memoized_property
    def rewards(self):
        """
        奖励
        """
        return [get_commonreward(rewardIdStr) for rewardIdStr in self.rewardIds_str.strip().split(",") if rewardIdStr]

    @memoized_property
    def diamondRewards(self):
        """
        钻石开箱奖励
        """
        return [get_commonreward(rewardIdStr) for rewardIdStr in self.diamondRewardIds_str.strip().split(",") if rewardIdStr]

    @memoized_property
    def diamondCosts(self):
        """
        钻石开箱消耗
        """
        return [int(float(cost)) for cost in self.diamondCosts_int.strip().split(",") if cost]

    @classmethod
    def get_instancelevel_by_tower_id(cls, tower_id):
        _cache_data = cls.get_list_by_foreignkey("towerId")
        return _cache_data[str(tower_id)] if str(tower_id) in _cache_data else []

    @memoized_property
    def enemies(self):
        return [Enemy.get(self.enemyId)]
