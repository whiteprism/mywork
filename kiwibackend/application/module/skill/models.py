# -*- coding: utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler
from rewards.models import RewardsBase
import copy
from common.decorators.memoized_property import memoized_property

class Skill(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"技能"
    name = models.CharField(u"技能名字", max_length=200)
    nameId = models.CharField(u"显示技能名字的id", max_length=200)
    confront = models.SmallIntegerField(u"是否需要面向攻击对象（转身）", default=0)
    #animation = models.CharField(u"wait cehua", max_length=200, default="")
    #animations_str = models.CharField(u"wait cehua", max_length=200, default="") # eg: 1,2,3,4
    #animationWeights_float = models.CharField(u"wait cehua", max_length=200,default="") #eg: 1,2,3,4
    attackDelay = models.FloatField(u"攻击延迟时间", default=0)
    attackingTime = models.FloatField(u"攻击动画开始造成伤害的时间点", default=0)
    attackingTimes_float = models.CharField(u"攻击动画开始造成伤害的时间点List", max_length=200, default="")
    attackCostTime = models.FloatField(u"攻击动画总时间", default=0)
    attackCostTimes_float = models.CharField(u"攻击动画总时间List", max_length=200, default="")
    attackType = models.SmallIntegerField(u"攻击类型", default=1)
    banFlags_int = models.CharField(u"当处在该flag的情况下，禁止释放该技能", max_length=200, default="")
    #branchInfo_int = models.CharField(u"分支技能", default="", max_length=200)
    #buffEffect = models.CharField(u"buff特效", default="", max_length=200)
    #buffEffectPonit = models.IntegerField(u"buff特效Point", default=0)
    coolDownTime = models.FloatField(u"技能冷却时间", default=0)
    deadEffectDelay = models.FloatField(u"播发死亡特效的延迟（秒）", default=0)
    deadEffect = models.CharField(u"死亡特效",max_length=200)
    #debuffEffect = models.CharField(u"debuff特效", default="", max_length=200)
    endEffect = models.CharField(u"技能结束特效",max_length=200, default="")
    energyCost = models.FloatField(u"大招消耗的能量", default=0)
    flyEffect = models.CharField(u"飞弹的特效", max_length=200, default="")
    gravity = models.FloatField(u"抛物线弹道的弧度（越大弧度越大）", default=0)
    #hasHitSound = models.SmallIntegerField(u"是否有打击音效", default=0)
    healEffect = models.CharField(u"加血特效", default="", max_length=200)
    hitPosition = models.IntegerField(u"受击位置")
    hitEffect = models.CharField(u"受击特效", default="",  max_length=200)
    hitEffectOffset = models.FloatField(u"受击特效偏移", default=0)
    hitSound = models.CharField(u"受击音效", default="", max_length=200)
    hurtDuration = models.FloatField(u"被击动画停顿时间", default=0)
    icon = models.CharField(u"图标", default="", max_length=200)
    interruptPower = models.IntegerField(u"打断强度",default=0)
    pathType = models.IntegerField(u"弹道类型",default=1)
    shakeCamera = models.BooleanField(u"是否振屏", default=False)
    shakeDelay = models.FloatField(u"屏震延迟", default=0)
    shakeDuration = models.FloatField(u"屏震时间", default=0)
    shakePower = models.CharField(u"屏震强度", default="", max_length=200)
    shakePowers_float = models.CharField(u"屏震强度List", default="", max_length=200) #skillId = models.IntegerField()
    spellExecuteType = models.IntegerField(u"攻击结果类型选取")
    spellType = models.IntegerField(u"攻击动画id")
    starSound = models.CharField(u"starSound", max_length=200)
    #startEffectDelay = models.FloatField(u"startEffectDelay")
    #startEffect = models.CharField(u"startEffect", max_length=200)
    steelArmorPower = models.IntegerField(u"steelArmorPower", default=1)
    targetGroup = models.SmallIntegerField(u"防御打断强度", default=0)
    targetPosition = models.SmallIntegerField(u"技能生效的阵营", default=1)
    targetPriority2 = models.SmallIntegerField(u"选取目标的位置优先度", default=0)
    targetPriority = models.IntegerField(u"技能打击的生效类型", default=0)
    triggerPossibility = models.FloatField(u"技能释放成功的概率", default=1)
    triggerType = models.IntegerField(u"技能释放规则", default=0)
    weaponSpeed = models.FloatField(u"飞弹的速度", default=0)
    weaponStartPositionXs_float = models.CharField(u"起手特效释放的相对位置偏移的X轴变量", max_length=200)
    weaponStartPositionYs_float = models.CharField(u"起手特效释放的相对位置偏移的Y轴变量", max_length=200)
    weaponStartPositionZs_float = models.CharField(u"起手特效释放的相对位置偏移的Z轴变量", max_length=200)
    knockDown = models.IntegerField(u"是否可以被击倒", default=0)
    isBlizzardType = models.IntegerField(u"是否是暴风雪类型", default=0)
    startPosType = models.IntegerField(u"弹道开始位置", default=0) #0-6
    targetHeroIds_int = models.CharField(u"圣物技能目标英雄列表", max_length=200, default=0)

    def __unicode__(self):
        return u"%s:%s" %(self.pk, self.name)

    def to_dict(self):
        dicts = super(Skill, self).to_dict()
        dicts["pk"] = self.pk
        levelConfs = SkillLevel.get_level_confs_by_skill(self)
        levelConfs.sort(key=lambda x: x.level)
        levelconfs_dict = {
            "affectHeight": [],
            "affectWidth": [],
            "apRate": [],
            "attackRate": [],
            #"autoSpellDelay": [],
            #"autoSpellDuration": [],
            #"autoSpellLevel": [],
            #"autoSpellType": [],
            "bounceCount": [],
            "bouncePower": [],
            "bounceRadius": [],
            "bounceTypeEnum":[],
            "costGold": [],
            "costs":[],
            "extraDamage":[],
            #"extras": [],
            "extraShoot": [],
            #"field0": [],
            #"field1": [],
            #"field2": [],
            #"field3": [],
            #"field4": [],
            #"field5": [],
            #"field6": [],
            "heroLevel": [],
            "initCD": [],
            "splashRadius": [],
            "weaponRepeatDelayTime":[],
            "weaponRepeatType": [],
            "weaponsCount": [],
            "effects": [],
            "level": [],
        }
        effect = {
            "conditionId": [],
            "extra0": [],
            "extra0Ability": [],
            "extra1": [],
            "extra1Ability":[],
            "extra2": [],
            "flags": [],
            "modifier": [],
            "registerMoment":[],
            "registerTarget": [],
            "targetSelector": [],

        }

        #几个技能特效初始化几个
        for i in range(0, len(levelConfs[0].to_dict()["effects"])):
            levelconfs_dict["effects"].append(copy.deepcopy(effect))
            
        for levelConf in levelConfs:
            levelConf = levelConf.to_dict()
            for k,v in levelConf.items():
                if k == "effects":
                    for i, _effect in enumerate(v):
                        for kk,vv in _effect.items():
                            if kk in  levelconfs_dict["effects"][i]:
                                levelconfs_dict["effects"][i][kk].append(vv)
                            
                elif k in levelconfs_dict:
                    levelconfs_dict[k].append(v)

        dicts["levelConfs"] = [levelconfs_dict]
            
        effectDetails  = SkillEffectDetail.get_effect_details_by_skill(self) 
        dicts["effectDetailList"] = [effectDetail.to_dict() for effectDetail in effectDetails]

        del dicts["id"]
        return dicts

class SkillLevel(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"技能等级"
    _CACHE_FKS = ["skill_id"]
    id = models.BigIntegerField(u"主键",primary_key = True)
    skill_id  = models.IntegerField(u"技能")
    affectHeight = models.FloatField(u"技能效果影响高度")
    affectWidth = models.FloatField(u"技能效果影响宽度")
    apRate = models.FloatField(u"法强倍率")
    attackRate = models.FloatField(u"攻强倍率")
    #autoSpellDelay = models.FloatField(u"自动技能延迟", default=0)
    #autoSpellDuration = models.FloatField(u"自动技能生效时间", default=0)
    #autoSpellLevel = models.IntegerField(u"自动技能等级",default=0)
    #autoSpellType = models.IntegerField(u"自动技能类型", default=0)
    bounceCount = models.IntegerField(u"弹射次数", default=0)
    bouncePower = models.FloatField(u"弹射倍率", default=0)
    bounceRadius = models.FloatField(u"弹射半径", default=0)
    bounceTypeEnum = models.IntegerField(u"弹射类型", default=0)
    costGold = models.IntegerField(u"消耗金币", default=0)
    costs_int = models.CharField(u"升级消耗物品", max_length=200)
    #costItemCount = models.IntegerField(u"消耗物品数量", default=0)
    extraDamage = models.FloatField(u"额外伤害", default=0)
    #extras_float = models.CharField(u"extras", default="", max_length=200)
    extraShoot = models.FloatField(u"extra shoot")
    #field0 = models.FloatField(u"field 0", default=0)
    #field1 = models.FloatField(u"field 1", default=0)
    #field2 = models.FloatField(u"field 2", default=0)
    #field3 = models.FloatField(u"field 3", default=0)
    #field4 = models.FloatField(u"field 4", default=0)
    #field5 = models.FloatField(u"field 5", default=0)
    #field6 = models.FloatField(u"field 6", default=0)
    heroLevel = models.IntegerField(u"英雄等级")
    initCD = models.FloatField(u"初始化持有cd")
    level = models.IntegerField(u"技能等级")
    splashRadius = models.FloatField(u"溅射")
    weaponRepeatDelayTime = models.FloatField(u"武器重复延迟")
    weaponRepeatType = models.IntegerField(u"武器重复类型")
    weaponsCount = models.IntegerField(u"weapons count")
    powerRank = models.IntegerField(u"战斗力", default=0)


    def __unicode__(self):
        return u"%s:%s(%s)" %( self.skill.name, self.pk, self.level)

    class Meta:
        ordering = ["id"]


    def __getattribute__(self, name):
        if name == 'skill':
            return self._related_skill
        return object.__getattribute__(self, name)

    @property
    def _related_skill(self):
        return Skill.get(self.skill_id)

    def to_dict(self):
        dicts = super(SkillLevel, self).to_dict()
        #dicts["pk"] = self.pk
        del dicts["id"]
        del dicts["skill_id"]
        skilleffects =  SkillEffect.get_effect_confs_by_skilllevel(self)
        dicts["effects"] = [skilleffect.to_dict() for skilleffect in skilleffects]
        dicts["costs"] = [cost.to_dict() for cost in self.costs]
        return dicts

    @memoized_property
    def costs(self):
        if self.costs_int.strip():

            for pk in self.costs_int.strip().split(","):
                if not SkillLevelUpCosts.get(pk):
                    print "this  pk", pk, "is null"

            return [SkillLevelUpCosts.get(pk) for pk in self.costs_int.strip().split(",")if pk]
        return []

    @classmethod
    def get_level_confs_by_skill(cls, skill_or_skill_id):
        if isinstance(skill_or_skill_id, Skill):
            skill_id = skill_or_skill_id.pk
        else:
            skill_id = int(skill_or_skill_id)

        
        _cache_data = cls.get_list_by_foreignkey("skill_id")
        return _cache_data[str(skill_id)] if str(skill_id) in _cache_data else {}
        #return cls.objects.filter(skill=skill)

    #@classmethod
    #def get_skilllevel(cls, skill_or_skill_id, level):
    #    skilllevels = cls.get_level_confs_by_skill(skill_or_skill_id)
    #    skilllevel = None
    #    for _sl in skilllevels:
    #        if _sl.level == level:
    #            skilllevel = _sl
    #            break
    #    return skilllevel
        
    @classmethod
    def get_skilllevels(cls, skill_or_skill_id):
        skilllevels = cls.get_level_confs_by_skill(skill_or_skill_id)
        return dict([(skilllevel.level, skilllevel) for skilllevel in skilllevels])

class SkillLevelUpCosts(RewardsBase):
    SHEET_NAME = u"技能升级消耗"

class SkillEffect(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"技能等级特效"
    _CACHE_FKS = ["skilllevel_id"]
    id = models.BigIntegerField(u"主键",primary_key = True)
    skilllevel_id = models.IntegerField(u"技能等级")
    conditionId = models.IntegerField(u"ConditionID", default=0)
    extra0 = models.FloatField(u"extra0")
    extra0Ability = models.IntegerField(u"extra0Ability" ,default=0)
    extra1 = models.FloatField(u"extra1", default=0)
    extra1Ability = models.IntegerField(u"extra1Ability", default=0)
    extra2 = models.FloatField(u"extra2", default=0)
    flags_int = models.CharField(u"skillflagid", max_length=200)
    modifier = models.IntegerField(u"特效类型")
    registerMoment = models.IntegerField(u"被动类型效果的生效时机")
    registerTarget = models.IntegerField(u"校验选择目标是否正确")
    targetSelector = models.IntegerField(u"效果最后选择目标")

    def __unicode__(self):
        return u"%s:%s" %( self.skilllevel.pk, self.pk)

    class Meta:
        ordering = ["id"]

    def __getattribute__(self, name):
        if name == 'skilllevel':
            return self._related_skilllevel
        return object.__getattribute__(self, name)

    @property
    def _related_skilllevel(self):
        return SkillLevel.get(self.skilllevel_id)
    
    def to_dict(self):
        dicts = super(SkillEffect, self).to_dict()
        del dicts["id"]
        del dicts["skilllevel_id"]
        return dicts

    @classmethod
    def get_effect_confs_by_skilllevel(cls, skilllevel):
        _cache_data = cls.get_list_by_foreignkey("skilllevel_id")
        return _cache_data[str(skilllevel.id)] if str(skilllevel.id) in _cache_data else {}


class Conditions(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"技能条件"
    condition_int = models.CharField(u"技能条件", default="", max_length=200)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = dicts["id"]

        _conditions = []
        for _c in dicts["condition"]:
            _condition = Condition.get(_c)
            if _condition:
                _conditions.append(_condition.to_dict())
        dicts["condition"] = _conditions

        del dicts["id"]
        return dicts

class Condition(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"技能条件详细"
    comparator = models.IntegerField(u"比较条件", default=0)
    leftAbility = models.IntegerField(u"左侧能力id", default=0)
    leftDouble = models.FloatField(u"左侧double类型变量数值", default=0)
    leftFloat = models.FloatField(u"左侧float类型变量数值", default=0)
    leftInt = models.IntegerField(u"左侧int类型变量数值", default=0)
    leftStr = models.CharField(u"左侧string类型变量数值", default="", max_length=200)
    leftVarEnum = models.IntegerField(u"左侧取值类型", default=0)
    rightAbility = models.IntegerField(u"右侧能力id", default=0)
    rightDouble = models.FloatField(u"右侧double类型变量数值", default=0)
    rightFloat = models.FloatField(u"右侧float类型变量数值", default=0)
    rightInt = models.IntegerField(u"右侧int类型变量数值" , default=0)
    rightStr = models.CharField(u"右侧string类型变量数值", default="", max_length=200)
    rightVarEnum = models.IntegerField(u"右侧取值类型", default=0)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        del dicts["id"]
        return dicts

class Flag(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"技能标示"
    effectName = models.CharField(u"特效名字", default="", max_length=200)
    effectSpecialShow = models.IntegerField(u"带有特殊效果的id")
    followBone = models.BooleanField(u"是否跟随骨骼")
    mountType = models.IntegerField(u"具体特效位置")
    offsetIgnoreType = models.IntegerField(u"特效根据模型胸部的偏移类型")
    nameId = models.CharField(u"对应该特效名字的对应id", default="", max_length=200)
    specialSkillId = models.IntegerField(u"specialSkillGid", default=0)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        del dicts["id"]
        dicts["pk"] = self.pk
        return dicts

class SkillEffectDetail(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"技能特效详细"
    _CACHE_FKS = ["skill_id"]
    skill_id = models.IntegerField(u"技能")
    #boneName = models.CharField(u"骨骼名称", default="", max_length=200)
    followPoint = models.BooleanField(u"是否跟随骨骼移动")
    socketIndex = models.IntegerField(u"特效播放的位置")
    startDelay = models.FloatField(u"播放延迟（秒）")
    startEffectName = models.CharField(u"起手特效名字", max_length=200)
    startPositionX = models.FloatField(u"起手特效位置的偏移量", default=0)
    startPositionY = models.FloatField(u"起手特效位置的偏移量", default=0)
    startPositionZ = models.FloatField(u"起手特效位置的偏移量", default=0)
    survivalTime = models.FloatField(u"特效播放总时间（秒）")

    def __unicode__(self):
        return u"%s:%s" %( self.skill.name, self.pk)

    class Meta:
        ordering = ["id"]

    def __getattribute__(self, name):
        if name == 'skill':
            return self._related_skill
        return object.__getattribute__(self, name)

    @property
    def _related_skill(self):
        return Skill.get(self.skill_id)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        del dicts["id"]
        del dicts["skill_id"]
        return dicts

    @classmethod
    def get_effect_details_by_skill(cls, skill):
        _cache_data = cls.get_list_by_foreignkey("skill_id")
        return _cache_data[str(skill.id)] if str(skill.id) in _cache_data else {}
