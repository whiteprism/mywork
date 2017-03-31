# -*- coding: utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler
from module.rewards.models import RewardsBase
from common.decorators.memoized_property import memoized_property

class BuildingType():
    CASTLE = 1001001 #部落要塞
    ALTAR  = 1001002 #召唤祭坛
    TARVEN = 1001003 #英雄圣殿
    BLACKSMITH = 1001004 #铁匠铺
    ARENA = 1001005 #角斗场
    GODESS = 1001006 #先祖祭坛
    BUNKER = 1001007 #地堡
    VAULT = 1001008 # 保险库
    GOLDMINE = 1001009 #金矿
    LOGGINGFIELD = 1001010 #伐木场
    HORDEBARRACK = 1001011 #部落兵营
    HORDELAB = 1001012 #战争图腾
    TAITAN = 1001013 #上古遗迹
    RADAR = 1001016 #全视之眼
    TOWER = 1002001 #防御塔
    ELEMENTTOWER = 1001014#元素之塔
    STATUE_GREEN_LV1 = 1004001 #绿色 生命
    STATUE_GREEN_LV2 = 1004002
    STATUE_GREEN_LV3 = 1004003
    STATUE_RED_LV1 = 1004004 #红色 攻击
    STATUE_RED_LV2 = 1004005
    STATUE_RED_LV3 = 1004006
    STATUE_BLUE_LV1 = 1004007 #蓝色 防御
    STATUE_BLUE_LV2 = 1004008
    STATUE_BLUE_LV3 = 1004009
    PLANT = 3 # 植物
    STATUE = 4 # 神像
    RAMPART = 1002002 # 城墙
    RAMPART_POINT = 1002003 # 城墙配置点


class Building(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"建筑"
    name = models.CharField(u"name", max_length=200, default="")
    nameId = models.CharField(u"nameId", max_length=200, default="")
    buildCamera = models.IntegerField(u"建造时是否对准", default=0)
    buildingToastId = models.CharField(u"玩家等级未达到时的提示信息", max_length=200, default="")
    category = models.IntegerField(u"建筑种类", default=0)
    descriptionId = models.CharField(u"desc", max_length=200, default="")
    orderId = models.IntegerField(u"排序", default=0)
    # width = models.IntegerField(u"宽度", default=0)
    # height = models.IntegerField(u"高度", default=0)
    model = models.CharField(u"模型", max_length=200, default="")
    summaryId = models.CharField(u"summaryId", max_length=200, default="")
    buildingToWarriorId = models.IntegerField(u"建筑对应的小兵Id", default=0)
    levelCount_int = models.CharField(u"奇数位等级，偶数位数量", max_length=200,default="")
    unlockUserLevel = models.IntegerField(u"玩家解锁等级", default=0)
    attrList_int = models.CharField(u"属性配置", max_length=100, default="")
    removeRewardIds_str = models.CharField(u"返还数量", max_length=200, default="")
    canRemove = models.BooleanField(u"是否可以被拆除", default=0)
    buildingPlantId = models.IntegerField(u"植物ID", default=0)

    @property
    def is_castle(self):
        return self.id == BuildingType.CASTLE

    @property
    def is_altar(self):
        return self.id == BuildingType.ALTAR

    @property
    def is_tarven(self):
        return self.id == BuildingType.TARVEN

    @property
    def is_blacksmith(self):
        return self.id == BuildingType.BLACKSMITH

    @property
    def is_arena(self):
        return self.id == BuildingType.ARENA

    @property
    def is_godess(self):
        return self.id == BuildingType.GODESS

    @property
    def is_goldmine(self):
        return self.id == BuildingType.GOLDMINE

    @property
    def is_loggingfield(self):
        return self.id == BuildingType.LOGGINGFIELD

    @property
    def is_taitan(self):
        return self.id == BuildingType.TAITAN

    @property
    def is_elementtower(self):
        return self.id == BuildingType.ELEMENTTOWER

    # @property
    # def is_deco(self):
    #     """
    #     装饰物
    #     """
    #     return self.category == 2

    @property
    def is_hordebarrack(self):
        return self.id == BuildingType.HORDEBARRACK

    @property
    def is_radar(self):
        return self.id == BuildingType.RADAR

    @property
    def is_tower(self):
        return self.id == BuildingType.TOWER

    @property
    def is_rampart(self):
        return self.id == BuildingType.RAMPART

    @property
    def is_rampart_point(self):
        return self.id == BuildingType.RAMPART_POINT 

    @classmethod
    def hordebarrack_soldiers(cls):
        """
        部落兵营可以生产的士兵
        """
        return [1900001,1900003,1900005, 1900007]
        
    @property
    def is_hordelab(self):
        return self.id == BuildingType.HORDELAB

    # TODO:没用上
    @property
    def can_drill_soldier(self):
        return self.is_hordebarrack 

    @property
    def can_upgrade_soldier(self):
        return self.is_hordelab

    @memoized_property
    def golden_levels(self):
        '''
        升级配置
        '''
        golden_levels = BuildingGolden.get_buildinggolden_by_building(self)
        return dict([(level.level, level) for level in golden_levels])

    @memoized_property
    def production_confs(self):
        return BuildingProduction.get_buildingproduction_by_building(self)
    @memoized_property
    def levelCount(self):
        return [int(float(i)) for i in self.levelCount_int.strip().split(",")  if i]

    @property
    def is_statue(self):
        if self.category == BuildingType.STATUE:
            return True
        return False

    @property
    def is_plant(self):
        if self.category == BuildingType.PLANT:
            return True
        return False

    @memoized_property
    def attrList(self):
        if self.attrList_int.strip():
            return [int(float(pk)) for pk in self.attrList_int.strip().split(",") if pk]
        return []

    @memoized_property
    def removeRewardIds(self):
        if self.removeRewardIds_str.strip():
            from rewards.api import get_commonreward
            return [get_commonreward(pk) for pk in self.removeRewardIds_str.strip().split(",") if pk]
        return []

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = self.pk
        _goldenMineConfs = BuildingGolden.get_buildinggolden_by_building(self)
        dicts["goldenMines"] = [_goldenMineConf.to_dict() for _goldenMineConf in _goldenMineConfs]
        _productionConfs = BuildingProduction.get_buildingproduction_by_building(self)
        dicts["productions"] = [_productionConf.to_dict() for _productionConf in _productionConfs]
        _upgradeconfs = BuildingUpgrade.get_buildingupgrade_by_building(self)
        dicts["upgrades"] = [_upgradeconf.to_dict() for _upgradeconf in _upgradeconfs]

        del dicts["id"]
        del dicts["name"]
        return dicts

class BuildingGolden(models.Model, StaticDataRedisHandler, CommonStaticModels):
    _CACHE_FKS = ["building_id"]
    SHEET_NAME = u"金矿"
    building_id = models.IntegerField(u"建筑ID", default=0)
    level = models.IntegerField(u"等级", default=0)
    minHarvestScale = models.IntegerField(u"可以执行采集所需的最小数量", default=0)
    productionPerHour = models.IntegerField(u"每小时产量", default=0)
    storage = models.IntegerField(u"最大存量", default=0)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        del dicts["id"]
        del dicts["building_id"]
        return dicts

    @classmethod
    def get_buildinggolden_by_building(cls, building_or_building_id):
        if isinstance(building_or_building_id, Building):
            building_id = building_or_building_id.pk
        else:
            building_id = int(building_or_building_id)

        _cache_data = cls.get_list_by_foreignkey("building_id")
        return _cache_data[str(building_id)] if str(building_id) in _cache_data else {}

class BuildingProduction(models.Model, StaticDataRedisHandler, CommonStaticModels):
    _CACHE_FKS = ["building_id"]
    SHEET_NAME = u"建筑产物"
    building_id = models.IntegerField(u"建筑ID", default=0)
    buildingLevel = models.IntegerField(u"等级", default=0)
    cost_int = models.CharField(u"消耗",max_length=200, default="")
    productionId = models.IntegerField(u"产物ID", default=0)
    productionLevel = models.IntegerField(u"产物等级", default=0)
    productionType = models.IntegerField(u"产物类型", default=0)
    useTime = models.IntegerField(u"消耗时间", default=0)
    icon = models.CharField(u"icon", max_length=200, default="")
    descriptionId = models.CharField(u"descriptionId", max_length=200, default="")
    nameId = models.CharField(u"nameId", max_length=200, default="")
    orderId = models.IntegerField(u"显示顺序", default=0)

    @property
    def is_drill(self):
        return self.productionType == 1

    @property
    def is_upgrade(self):
        return self.productionType == 2

    @memoized_property
    def cost(self):
        return [BuildingProductionCost.get(pk) for pk in self.cost_int.strip().split(",") if pk]

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["cost"] = [_c.to_dict() for _c in self.cost]
        del dicts["id"]
        del dicts["building_id"]
        return dicts

    @classmethod
    def get_buildingproduction_by_building(cls, building_or_building_id):
        if isinstance(building_or_building_id, Building):
            building_id = building_or_building_id.pk
        else:
            building_id = int(building_or_building_id)

        _cache_data = cls.get_list_by_foreignkey("building_id")
        return _cache_data[str(building_id)] if str(building_id) in _cache_data else {}

class BuildingProductionCost(RewardsBase):
    SHEET_NAME = u"建筑产物消耗"

class BuildingUpgrade(models.Model, StaticDataRedisHandler, CommonStaticModels):
    _CACHE_FKS = ["building_id"]
    SHEET_NAME = u"建筑升级"
    building_id = models.IntegerField(u"建筑ID", default=0)
    costs_int = models.CharField(u"消耗",max_length=200, default="")
    level = models.IntegerField(u"等级", default=0)
    castleLevel = models.IntegerField(u"主城等级", default=0)
    userLevel = models.IntegerField(u"用户等级", default=0)
    useTime = models.IntegerField(u"花费时间", default=0)

    @memoized_property
    def costs(self):
        return [BuildingUpgradeCost.get(pk) for pk in self.costs_int.strip().split(",") if pk]

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["cost"] = [_c.to_dict() for _c in self.costs]
        del dicts["id"]
        del dicts["building_id"]
        return dicts

    @classmethod
    def get_buildingupgrade_by_building(cls, building_or_building_id):
        if isinstance(building_or_building_id, Building):
            building_id = building_or_building_id.pk
        else:
            building_id = int(building_or_building_id)

        _cache_data = cls.get_list_by_foreignkey("building_id")
        return _cache_data[str(building_id)] if str(building_id) in _cache_data else {}

class BuildingUpgradeCost(RewardsBase):
    SHEET_NAME = u"建筑升级消耗"

class BuildingResourceProtected(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"资源保护"
    building_id = models.IntegerField(u"建筑id", default=0)
    level = models.IntegerField(u"等级", default=0)
    goldCount = models.IntegerField(u"保护金币数量", default=0)
    woodCount = models.IntegerField(u"保护木头数量", default=0)
    percentage = models.FloatField(u"保护数量百分比", default=0)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["id"] = self.building_id
        return dicts

class BuildingRadar(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"雷达"
    building_id = models.IntegerField(u"建筑id", default=0)
    level = models.IntegerField(u"等级", default=0)
    count = models.IntegerField(u"增加搜索数量", default=0)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["id"] = self.building_id
        return dicts

class BuildingGoldHand(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"点金手"

    critTwo = models.IntegerField(u"两倍暴击概率", default=0)
    critThree = models.IntegerField(u"三倍暴击概率", default=0)
    critFive = models.IntegerField(u"五倍暴击概率", default=0)
    critTen = models.IntegerField(u"十倍暴击概率", default=0)
    critProperbility = models.IntegerField(u"是否暴击概率", default=0)
    expectGold = models.IntegerField(u"预计金额", default=0)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        return dicts

class BuildingFragment(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"建筑碎片"

    name = models.CharField(u"name", max_length=200, default=0)
    buildingId = models.IntegerField(u"合成后建筑ID", default=0)
    nameId = models.CharField(u"nameId", max_length=200, default="")
    icon = models.CharField(u"icon", max_length=200, default="")
    descriptionId = models.CharField(u"descriptionId", max_length=200, default="")
    searchDifficuty_int = models.CharField(u"掉落关卡难度", max_length=200, default="")
    searchInstances_int = models.CharField(u"掉落关卡", max_length=200, default="")

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["gid"] = self.pk
        del dicts["id"]
        del dicts["name"]
        return dicts

class BuildingAttribute(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"建筑属性"
    
    attrType = models.CharField(u"attrType", max_length=200)
    minValue = models.FloatField(u"最小值", default=0)
    maxValue = models.FloatField(u"最大值", default=0)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        return dicts

class PlantType():
    FLOWER = 1
    TREE = 2

class BuildingPlant(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"建筑植物"

    costRewardId = models.CharField(u"种子ID", max_length=100, default="")
    rewardIds_str = models.CharField(u"产物", max_length=100, default="")
    harvestTimes = models.IntegerField(u"可采摘的次数", default=0)
    harvestInterval = models.IntegerField(u"采摘的时间间隔", default=0)
    growthInterval = models.IntegerField(u"幼苗到成长时间间隔", default=0)
    matureInterval = models.IntegerField(u"成长到成熟时间间隔", default=0)
    category = models.IntegerField(u"植物种类", default=0)
    
    @property
    def is_flower(self):
        return self.category == PlantType.FLOWER

    @property
    def is_tree(self):
        return self.category == PlantType.TREE

    @property
    def costs(self):
        if self.costRewardId.strip():
            from rewards.api import get_commonreward
            return [get_commonreward(pk) for pk in self.costRewardId.strip().split(",") if pk]
        return []

    @property
    def rewards(self):
        if self.rewardIds_str.strip():
            from rewards.api import get_commonreward
            return [get_commonreward(pk) for pk in self.rewardIds_str.strip().split(",") if pk]
        return []

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        del dicts["costRewardId"]
        return dicts
