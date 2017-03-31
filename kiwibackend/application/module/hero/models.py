# -*- coding: utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
#from common.models import CommonStaticUnitModels, CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler
#from rewards.api import get_hero_eveolve_cost
from rewards.models import RewardsBase
from module.common.static import Static
from common.decorators.memoized_property import memoized_property

class Card(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"英雄种族"
    name = models.CharField(u"英雄名称", max_length=200)
    warrior_id = models.IntegerField(u"初始化英雄")
    career = models.IntegerField(u"职业")
    equipFates_int = models.CharField(u"装备缘分", max_length=200, default="")

    @memoized_property
    def warrior(self):
        return Warrior.get(self.warrior_id)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        return dicts

# class HeroEquipFatesAttr(models.Model, StaticDataRedisHandler, CommonStaticModels):
#     SHEET_NAME = u"英雄装备缘分属性"
#     equipId = models.IntegerField(u"装备id",default=0)
#     attrType = models.CharField(u"属性类别", max_length=200)
#     extra = models.FloatField(u"属性提升", default=0)

class Hero(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"英雄"
    cardId = models.IntegerField(u"英雄ID ", default=0)
    name = models.CharField(u"英雄名称", max_length=200)
    upgrade = models.IntegerField(u"进阶加几")
    evolveHero_id = models.IntegerField(u"进阶目标英雄", default=0)
    evolveLevel = models.IntegerField(u"evolveLevel", default=0)
    evolveSoulCost = models.IntegerField(u"evolveSoulCount", default=0)
    evolveCosts_int = models.CharField(u"evolveCosts", max_length=100, default="")
    soulId = models.IntegerField(u"soulId", default=0)
    maxLevel = models.IntegerField(u"maxLevel")
    attack = models.FloatField(u"基础攻强")
    # trainAttackMax = models.FloatField(u"培养攻强上限" ,default=0)
    hp = models.FloatField(u"基础血量")
    # trainHpMax = models.FloatField(u"培养血量上限" ,default=0)
    physicalArmor = models.FloatField(u"基础物防")
    # trainPhysicalArmorMax = models.FloatField(u"培养物防上限", default=0)
    magicArmor = models.FloatField(u"基础法防")
    # trainMagicArmorMax = models.FloatField(u"培养法防上限", default=0)
    realPhysical = models.FloatField(u"穿甲", default=0)
    realMagic = models.FloatField(u"法穿", default=0)
    shoot = models.FloatField(u"基础命中")
    dodge = models.FloatField(u"基础闪避")
    critical = models.FloatField(u"基础暴击")
    tenacity = models.FloatField(u"基础韧性")
    damageFree = models.FloatField(u"额外减伤")
    powerRank = models.FloatField(u"基础战斗力", default=0)
    energyPerSec = models.FloatField(u"每秒回能")
    maxEnergy = models.IntegerField(u"最大能量")
    quality = models.IntegerField(u"品质", default=0)
    category = models.IntegerField(u"分类", default=0)
    violence = models.FloatField(u"暴击倍率")
    killToHeal = models.FloatField(u"击杀回血")
    killToEnergy = models.FloatField(u"击杀回能")
    hpPerSecond = models.FloatField(u"每秒回血")
    heroTeamId = models.IntegerField(u"英雄组id", default=0)
    hurtToEnergy = models.FloatField(u"收集回能", default=0)

    def __unicode__(self):
        return u"%s:%s:%s" %(self.pk, self.name, self.upgrade)

    class Meta:
        ordering = ["id"]

    @property
    def is_white(self):
        return self.upgrade == 0

    @property
    def is_green(self):
        return self.upgrade == 1

    @property
    def is_green_plus_1(self):
        return self.upgrade == 2

    @property
    def is_green_plus_2(self):
        return self.upgrade == 3

    @property
    def is_blue(self):
        return self.upgrade == 4

    @property
    def is_blue_plus_1(self):
        return self.upgrade == 5

    @property
    def is_blue_plus_2(self):
        return self.upgrade == 6

    @property
    def is_blue_plus_3(self):
        return self.upgrade == 7

    @property
    def is_purple(self):
        return self.upgrade == 8

    @property
    def is_purple_plus_1(self):
        return self.upgrade == 9

    @property
    def is_purple_plus_2(self):
        return self.upgrade == 10

    @property
    def is_purple_plus_3(self):
        return self.upgrade == 11

    @memoized_property
    def evolveCosts(self):
        if self.evolveCosts_int.strip():
            return [HeroEvolveCosts.get(pk) for pk in self.evolveCosts_int.strip().split(",")if pk]
        return []

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        del dicts["id"]
        del dicts["name"]
        del dicts["evolveHero_id"]

        for hero_evolve_cost in self.evolveCosts:
            if not hero_evolve_cost:
                print self.id, u"这个英雄里面配置的evolveCosts　在进阶消耗表里面没有"


        dicts["evolveCosts"] = [hero_evolve_cost.to_dict() for hero_evolve_cost in self.evolveCosts]
        return dicts

class HeroStar(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"英雄升星成长"
    cardId = models.IntegerField(u"英雄ID", default=0)
    star = models.IntegerField(u"英雄星级", default=0)
    attackGrow = models.FloatField(u"攻击力成长", default=0)
    hpGrow = models.FloatField(u"血量成长", default=0)
    physicalArmorGrow = models.FloatField(u"护甲成长", default=0)
    magicArmorGrow = models.FloatField(u"魔抗成长", default=0)
    realPhysicalGrow = models.FloatField(u"物穿成长", default=0)
    realMagicGrow = models.FloatField(u"法穿成长", default=0)
    shootGrow = models.FloatField(u"命中成长", default=0)
    dodgeGrow = models.FloatField(u"闪避成长", default=0)
    criticalGrow = models.FloatField(u"暴击成长", default=0)
    tenacityGrow = models.FloatField(u"韧性成长", default=0)
    damageFreeGrow = models.FloatField(u"额外减伤成长", default=0)
    energyPerSecGrow = models.FloatField(u"每秒回能成长", default=0)
    growPercent = models.FloatField(u"成长百分比", default=0)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = self.id
        dicts["heroId"] = self.cardId
        del dicts["id"]
        return dicts

class Warrior(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"小兵"
    name = models.CharField(u"英雄名称", max_length=200)
    cardId = models.IntegerField(u"cardId as gid")
    attackedPoint = models.CharField(u"attackedPoint", default="", max_length=200)
    attackRange = models.IntegerField(u"attackRange", default=0)
    attackSpan = models.IntegerField(u"attackSpan", default=0)
    category = models.IntegerField(u"卡的类型（小兵还是英雄）")
    chestPositionX = models.FloatField(u"胸部位置偏移量", default=0)
    chestPositionY = models.FloatField(u"胸部位置偏移量", default=0)
    chestPositionZ = models.FloatField(u"胸部位置偏移量", default=0)
    deadBonePoint_char = models.CharField(u"死亡特效位置", max_length=200)
    deadEffect_char = models.CharField(u"死亡特效", default="", max_length=200)
    deadEffectDelay_float = models.CharField(u"死亡特效延迟", default=0, max_length=200)
    descriptionId = models.CharField(u"descId", default=0, max_length=200)
    height = models.IntegerField(u"高度")
    hurtRate = models.FloatField(u"受击时间倍率")
    downRate = models.FloatField(u"被击倒时间倍率", default=1)
    icon = models.CharField(u"图标", default="", max_length=200)
    modelName = models.CharField(u"模型名称", max_length=200)
    moveActRate = models.FloatField(u"moveActRate", default=0)
    moveSpeed = models.FloatField(u"移动速度")
    nameId = models.CharField(u"nameId", max_length=200)
    population = models.IntegerField(u"population", default=0)
    width = models.IntegerField(u"宽度")
    nextWarriorID = models.IntegerField(u"小兵下一个形态小兵ID", default=0)
    nextWarriorLevel = models.IntegerField(u"小兵下个形态小兵等级", default=0)
    searchRange = models.FloatField(u"寻怪", default=0)
    maxCount = models.IntegerField(u"最大投放数量", default=0)
    attackType = models.IntegerField(u"攻击类型", default=0) #1 魔法攻击 0 物理攻击

    @memoized_property
    def quality(self):
        if self.is_hero:
            return self.hero.quality
        return 0

    @memoized_property
    def levels(self):
        return WarriorLevel.get_warriorlevels_by_warrior(self)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = dicts["cardId"]

        if self.is_hero:
            dicts["hero"] = self.hero.to_dict()
        else:
            dicts["hero"] = None

        if not self.is_hero:
            dicts["warriorLevel"] = [_w.to_dict() for _w in self.levels]

        del dicts["cardId"]
        del dicts["name"]
        del dicts["id"]
        return dicts

    @property
    def is_warrior(self):
        return self.category in Static.HERO_WARRIOR_CATEGORY_WARRIOR

    @property
    def is_hero(self):
        return self.category == Static.HERO_WARRIOR_CATEGORY_HERO

    @property
    def is_boss(self):
        return self.category == Static.HERO_WARRIOR_CATEGORY_BOSS

    @property
    def is_wall(self):
        return self.category == Static.HERO_WARRIOR_CATEGORY_WALL

    @memoized_property
    def hero(self):
        return Hero.get(self.id)

    def is_wallsoldier():
        '''
            科技树中的士兵（城墙士兵）
        '''
        return self.warrior_id in Static.HERO_WALL_SOLDIER_IDS

class WarriorLevel(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"小兵等级"
    _CACHE_FKS = ["warrior_id"]
    id = models.BigIntegerField(u"主键", primary_key = True)
    warrior_id = models.IntegerField(u"小兵ID")
    ap = models.FloatField(u"法强")
    attack = models.FloatField(u"攻强")
    hp = models.FloatField(u"生命")
    magicArmor = models.FloatField(u"魔抗")
    physicalArmor = models.FloatField(u"护甲")
    powerRank = models.IntegerField(u"powerRank", default=0)
    level = models.IntegerField(u"等级")
    shoot = models.FloatField(u"命中")
    skills_int = models.CharField(u"skills", max_length=200, default="")
    skill0 = models.IntegerField(u"skill0", default=0)
    skill0Lv = models.IntegerField(u"skill0Lv", default=0)
    dodge = models.FloatField(u"闪避")
    tenacity = models.FloatField(u"韧性")
    critical = models.FloatField(u"暴击")
    violence = models.FloatField(u"暴击倍率")
    hpPerSecond = models.FloatField(u"每秒回血")

    class Meta:
        ordering = ["id"]

    @memoized_property
    def warrior(self):
        return Warrior.get(self.pk)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        return dicts

    @classmethod
    def get_warriorlevels_by_warrior(cls, warrior_or_warrior_id):
        if isinstance(warrior_or_warrior_id, Warrior):
            warrior_id = warrior_or_warrior_id.pk
        else:
            warrior_id = int(warrior_or_warrior_id)

        _cache_data = cls.get_list_by_foreignkey("warrior_id")
        return _cache_data[str(warrior_id)] if str(warrior_id) in _cache_data else {}

class HeroSkill(models.Model, StaticDataRedisHandler, CommonStaticModels):
    """
    卡牌技能
    id : warrior 主键
    """
    SHEET_NAME = u"英雄技能"
    maxStar = models.IntegerField(u"maxStar")
    #passiveSkill_int = models.CharField(u"passiveSkill_int", default="", max_length=200)
    skill0 = models.IntegerField(u"skill0")
    skill0Lv = models.IntegerField(u"skill0Lv")
    skillinfo_int = models.CharField(u"skillinfo_int", default="", max_length=200)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        del dicts["id"]
        dicts["pk"] = self.pk
        return dicts

    @property
    def skillinfo(self):
        if self.skillinfo_int.strip():
            return [int(i) for i in self.skillinfo_int.strip().split(",")]
        return []

class HeroEvolveCosts(RewardsBase):
    SHEET_NAME = u"英雄进阶消耗"

class HeroLevel(models.Model, StaticDataRedisHandler, CommonStaticModels):
    """
    英雄升级
    """
    SHEET_NAME = u"英雄升级"
    xp = models.IntegerField(u"xp")

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["level"] = self.pk #从1开始计算
        del dicts["id"]
        return dicts

class HeroStarUpgrade(models.Model, StaticDataRedisHandler, CommonStaticModels):
    """
    英雄升星
    """
    SHEET_NAME = u"英雄升星"
    soulCount = models.IntegerField(u"消耗soul数量")
    costs_int = models.CharField(u"costs", max_length=100, default="")
    sepecialItemMaxCount = models.IntegerField(u"消耗特殊物品数量上限")

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["star"] = self.pk #从0开始计算
        dicts["costs"] = [cost.to_dict() for cost in self.costs]
        del dicts["id"]
        return dicts

    @memoized_property
    def costs(self):
        if self.costs_int.strip():
            return [HeroStarUpgradeCosts.get(pk) for pk in self.costs_int.strip().split(",") if pk]
        return []

class HeroStarUpgradeCosts(RewardsBase):
    SHEET_NAME = u"英雄升星消耗"

class HeroMaster(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"英雄成长大师"
    _CACHE_FKS = ["category"]
    category = models.IntegerField(u"类别", default=0)
    level = models.IntegerField(u"等级", default=0)
    attrList_int = models.CharField(u"属性配置", max_length=100, default="")
    descriptionId = models.CharField(u"描述信息", max_length=100, default="")

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["attrList"] = [_equipattr.to_dict() for _equipattr in self.attrList]
        return dicts

    @memoized_property
    def attrList(self):
        if self.attrList_int.strip():
            return [HeroAttribute.get(int(float(pk))) for pk in self.attrList_int.strip().split(",") if pk]
        return []

    @classmethod
    def get_heromasters_by_catergory(cls, category):
        _cache_data = cls.get_list_by_foreignkey("category")
        return _cache_data[str(category)] if str(category) in _cache_data else []

class HeroAttribute(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"英雄大师属性"
    attrType = models.CharField(u"attrType", max_length=200)
    extra = models.FloatField(u"extra", default=0)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        del dicts["id"]
        return dicts

class HeroDestiny(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"英雄天命"
    level = models.IntegerField(u"天命等级", default=1)
    stoneCost = models.IntegerField(u"消耗天命石", default=0)
    heroLevel = models.IntegerField(u"需要玩家的等级", default=0)
    extra = models.FloatField(u"属性成长", default=0)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        del dicts["id"]
        return dicts

# class HeroTrain(models.Model, StaticDataRedisHandler, CommonStaticModels):
#     SHEET_NAME = u"英雄培养"
#     count = models.IntegerField(u"消耗培养丹的数量", default=0)
#     goldCost = models.IntegerField(u"消耗金币的数量", default=0)
#     diamondCost = models.IntegerField(u"消耗钻石的数量", default=0)
#     hpAttrValues_int = models.CharField(u"血量属性的增加减少值", max_length=500, default="")
#     magicAttrValues_int = models.CharField(u"魔法防御属性的增加减少值", max_length=500, default="")
#     physicalAttrValues_int = models.CharField(u"物理防御属性的增加减少值", max_length=500, default="")
#     attackAttrValues_int = models.CharField(u"攻击属性的增加减少值", max_length=500, default="")
#     itemProbabilities_int = models.CharField(u"培养丹对应属性的权重", max_length=100, default="")
#     goldProbabilities_int = models.CharField(u"金币对应属性的权重", max_length=100, default="")
#     diamondProbabilities_int = models.CharField(u"钻石对应属性的权重", max_length=100, default="")

#     def to_dict(self):
#         dicts = super(self.__class__, self).to_dict()
#         dicts["pk"] = self.pk
#         del dicts["id"]
#         return dicts

#     @memoized_property
#     def attackAttrValues(self):
#         return [int(float(value)) for value in self.attackAttrValues_int.strip().split(",") if value]

#     @memoized_property
#     def physicalAttrValues(self):
#         return [int(float(value)) for value in self.physicalAttrValues_int.strip().split(",") if value]
#     @memoized_property
#     def magicAttrValues(self):
#         return [int(float(value)) for value in self.magicAttrValues_int.strip().split(",") if value]

#     @memoized_property
#     def hpAttrValues(self):
#         return [int(float(value)) for value in self.hpAttrValues_int.strip().split(",") if value]

#     @memoized_property
#     def itemProbabilities(self):
#         return [int(float(itemProbability)) for itemProbability in self.itemProbabilities_int.strip().split(",") if itemProbability]

#     @memoized_property
#     def goldProbabilities(self):
#         return [int(float(goldProbability)) for goldProbability in self.goldProbabilities_int.strip().split(",") if goldProbability]

#     @memoized_property
#     def diamondProbabilities(self):
#         return [int(float(diamondProbability)) for diamondProbability in self.diamondProbabilities_int.strip().split(",") if diamondProbability]

#     @memoized_property
#     def train_attackvalues_item(self):
#         return zip(self.attackAttrValues, self.itemProbabilities)

#     @memoized_property
#     def train_attackvalues_gold(self):
#         return zip(self.attackAttrValues, self.goldProbabilities)

#     @memoized_property
#     def train_attackvalues_diamond(self):
#         return zip(self.attackAttrValues, self.diamondProbabilities)

#     @memoized_property
#     def train_physicalvalues_item(self):
#         return zip(self.physicalAttrValues, self.itemProbabilities)

#     @memoized_property
#     def train_physicalvalues_gold(self):
#         return zip(self.physicalAttrValues, self.goldProbabilities)

#     @memoized_property
#     def train_physicalvalues_diamond(self):
#         return zip(self.physicalAttrValues, self.diamondProbabilities)

#     @memoized_property
#     def train_magicvalues_item(self):
#         return zip(self.magicAttrValues, self.itemProbabilities)

#     @memoized_property
#     def train_magicvalues_gold(self):
#         return zip(self.magicAttrValues, self.goldProbabilities)

#     @memoized_property
#     def train_magicvalues_diamond(self):
#         return zip(self.magicAttrValues, self.diamondProbabilities)

#     @memoized_property
#     def train_hpvalues_item(self):
#         return zip(self.hpAttrValues, self.itemProbabilities)

#     @memoized_property
#     def train_hpvalues_gold(self):
#         return zip(self.hpAttrValues, self.goldProbabilities)

#     @memoized_property
#     def train_hpvalues_diamond(self):
#         return zip(self.hpAttrValues, self.diamondProbabilities)

#     def train_attackvalues(self, train_type):
#         if train_type == 1:
#             return self.train_attackvalues_item
#         elif train_type == 2:
#             return self.train_attackvalues_gold
#         elif train_type == 3:
#             return self.train_attackvalues_diamond
#         return []

#     def train_physicalvalues(self, train_type):
#         if train_type == 1:
#             return self.train_physicalvalues_item
#         elif train_type == 2:
#             return self.train_physicalvalues_gold
#         elif train_type == 3:
#             return self.train_physicalvalues_diamond
#         return []

#     def train_magicvalues(self, train_type):
#         if train_type == 1:
#             return self.train_magicvalues_item
#         elif train_type == 2:
#             return self.train_magicvalues_gold
#         elif train_type == 3:
#             return self.train_magicvalues_diamond
#         return []

#     def train_hpvalues(self, train_type):
#         if train_type == 1:
#             return self.train_hpvalues_item
#         elif train_type == 2:
#             return self.train_hpvalues_gold
#         elif train_type == 3:
#             return self.train_hpvalues_diamond
#         return []

class HeroTeam(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"英雄分组"
    heroCardIds_int = models.CharField(u"相应组里面所有英雄cardid", max_length=100, default="")
    descriptionId = models.CharField(u"descId", default=0, max_length=200)
    nameId = models.CharField(u"nameId", default=0, max_length=200)
    name = models.CharField(u"name", default=0, max_length=200)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = self.pk
        del dicts["id"]
        return dicts

    @memoized_property
    def heroCardIds(self):
        return [pk for pk in self.heroCardIds_int.strip().split(",") if pk]

class HeroTeamLevel(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"英雄组级别"
    teamId = models.IntegerField(u"英雄组的Id", default=0)
    level = models.IntegerField(u"英雄组的级别", default=0)
    score = models.IntegerField(u"英雄组的积分", default=0)
    costs_int = models.CharField(u"英雄组升级的消耗", max_length=100, default=0)
    attrList_int = models.CharField(u"属性配置", max_length=100, default="")
    nextLevelId = models.IntegerField(u"下一个级别的主键", default=0)


    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = self.pk
        dicts["attrList"] = [_attr.to_dict() for _attr in self.attrList]
        dicts["costs"] = [_c.to_dict() for _c in self.costs]
        del dicts["id"]
        return dicts


    @memoized_property
    def costs(self):
        return [HeroTeamLevelCost.get(pk) for pk in self.costs_int.strip().split(",") if pk]


    @memoized_property
    def attrList(self):
        if self.attrList_int.strip():
            return [HeroTeamAttribute.get(int(float(pk))) for pk in self.attrList_int.strip().split(",") if pk]
        return []


class HeroTeamAttribute(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"英雄组属性"
    attrType = models.CharField(u"attrType", max_length=200)
    extra = models.FloatField(u"extra", default=0)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        del dicts["id"]
        return dicts

class HeroTeamLevelCost(RewardsBase):
    SHEET_NAME = u"组队升级消耗"



class HeroBubble(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"英雄气泡表"
    heroId = models.IntegerField(u"英雄的Id", default=0)

    bornTypeMessage_str = models.CharField(max_length=500)
    initPointTypeMessage_str = models.CharField(max_length=500)
    gatherPointTypeMessage_str = models.CharField(max_length=500)
    initAttackTypeMessage_str = models.CharField(max_length=500)
    strokesTypeMessage_str = models.CharField(max_length=500)
    hpLowTypeMessage_str = models.CharField(max_length=500)
    friendsHpLowTypeMessage_str = models.CharField(max_length=500)
    deadTypeMessage_str = models.CharField(max_length=500)
    friendsDeadTypeMessage_str = models.CharField(max_length=500)
    normalAttackTypeMessage_str = models.CharField(max_length=500)
    sneerTypeMessage_str = models.CharField(max_length=500)

    bornTypeProperbility = models.FloatField(default=0.0)
    initPointTypeProperbility = models.FloatField(default=0.0)
    gatherPointTypeProperbility = models.FloatField(default=0.0)
    initAttackTypeProperbility = models.FloatField(default=0.0)
    strokesTypeProperbility = models.FloatField(default=0.0)
    hpLowTypeProperbility = models.FloatField(default=0.0)
    friendsHpLowTypeProperbility = models.FloatField(default=0.0)
    deadTypeProperbility = models.FloatField(default=0.0)
    friendsDeadTypeProperbility = models.FloatField(default=0.0)
    normalAttackTypeProperbility = models.FloatField(default=0.0)
    sneerTypeProperbility = models.FloatField(default=0.0)



    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        del dicts["id"]
        return dicts

    @memoized_property
    def bornTypeMessage(self):
        return [pk for pk in self.bornTypeMessage_str.strip().split(",") if pk]

    @memoized_property
    def initPointTypeMessage(self):
        return [pk for pk in self.initPointTypeMessage_str.strip().split(",") if pk]

    @memoized_property
    def gatherPointTypeMessage(self):
        return [pk for pk in self.gatherPointTypeMessage_str.strip().split(",") if pk]

    @memoized_property
    def initAttackTypeMessage(self):
        return [pk for pk in self.initAttackTypeMessage_str.strip().split(",") if pk]

    @memoized_property
    def strokesTypeMessage(self):
        return [pk for pk in self.strokesTypeMessage_str.strip().split(",") if pk]

    @memoized_property
    def hpLowTypeMessage(self):
        return [pk for pk in self.hpLowTypeMessage_str.strip().split(",") if pk]

    @memoized_property
    def friendsHpLowTypeMessage(self):
        return [pk for pk in self.friendsHpLowTypeMessage_str.strip().split(",") if pk]

    @memoized_property
    def deadTypeMessage(self):
        return [pk for pk in self.deadTypeMessage_str.strip().split(",") if pk]

    @memoized_property
    def friendsDeadTypeMessage(self):
        return [pk for pk in self.friendsDeadTypeMessage_str.strip().split(",") if pk]

    @memoized_property
    def normalAttackTypeMessage(self):
        return [pk for pk in self.normalAttackTypeMessage_str.strip().split(",") if pk]

    @memoized_property
    def sneerTypeMessage(self):
        return [pk for pk in self.sneerTypeMessage_str.strip().split(",") if pk]

class HeroCombat(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"英雄战斗力参考表"
    atk = models.FloatField(default=0.0)
    hp = models.FloatField(default=0.0)
    armor = models.FloatField(default=0.0)
    magArmor = models.FloatField(default=0.0)
    phyPenetr = models.FloatField(default=0.0)
    magPenetr = models.FloatField(default=0.0)
    hitin = models.FloatField(default=0.0)
    dodge = models.FloatField(default=0.0)
    crit = models.FloatField(default=0.0)
    toughness = models.FloatField(default=0.0)
    etrAtkReduc  = models.FloatField(default=0.0)
    energy = models.FloatField(default=0.0)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = self.pk
        return dicts
