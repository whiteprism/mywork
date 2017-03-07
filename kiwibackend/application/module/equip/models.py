# -*- coding: utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler
from common.decorators.memoized_property import memoized_property

class CardEquipInfo(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"种族装备"
    pos1_int = models.CharField(u"位置1", max_length=300)
    pos2_int = models.CharField(u"位置2", max_length=300)
    pos3_int = models.CharField(u"位置3", max_length=300)
    pos4_int = models.CharField(u"位置4", max_length=300)
    pos5_int = models.CharField(u"位置5", max_length=300)
    pos6_int = models.CharField(u"位置6", max_length=300)

    @property
    def pos1(self):
        return [int(float(equip_id)) for equip_id in self.pos1_int.strip().split(",") if equip_id]
    @property
    def pos2(self):
        return [int(float(equip_id)) for equip_id in self.pos2_int.strip().split(",") if equip_id]
    @property
    def pos3(self):
        return [int(float(equip_id)) for equip_id in self.pos3_int.strip().split(",") if equip_id]
    @property
    def pos4(self):
        return [int(float(equip_id)) for equip_id in self.pos4_int.strip().split(",") if equip_id]
    @property
    def pos5(self):
        return [int(float(equip_id)) for equip_id in self.pos5_int.strip().split(",") if equip_id]
    @property
    def pos6(self):
        return [int(float(equip_id)) for equip_id in self.pos6_int.strip().split(",") if equip_id]

class EquipSuit(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"装备套装"
    nameId = models.CharField(u"nameId", max_length=200, default="")
    pos1Id =  models.IntegerField(u"武器")
    pos2Id =  models.IntegerField(u"头盔")
    pos3Id =  models.IntegerField(u"衣服")
    pos4Id =  models.IntegerField(u"裤子")
    attr2List_int = models.CharField(u"2件装备属性加成", max_length=200)
    attr3List_int = models.CharField(u"3件装备属性加成", max_length=200)
    attr4List_int = models.CharField(u"4件装备属性加成", max_length=200)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["attr2List"] = [_attr.to_dict() for _attr in self.attr2List]
        dicts["attr3List"] = [_attr.to_dict() for _attr in self.attr3List]
        dicts["attr4List"] = [_attr.to_dict() for _attr in self.attr4List]
        dicts["pk"] = dicts["id"]
        del dicts["id"]
        return dicts

    @memoized_property
    def attr2List(self):
        if self.attr2List_int.strip():
            return [EquipSuitAttr.get(float(pk)) for pk in self.attr2List_int.strip().split(",") if pk]
        return []

    @memoized_property
    def attr3List(self):
        if self.attr3List_int.strip():
            return [EquipSuitAttr.get(float(pk)) for pk in self.attr3List_int.strip().split(",") if pk]
        return []
    
    @memoized_property
    def attr4List(self):
        if self.attr4List_int.strip():
            return [EquipSuitAttr.get(float(pk)) for pk in self.attr4List_int.strip().split(",") if pk]
        return []

class EquipSuitAttr(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"装备套装属性"
    attrType = models.CharField(u"attrType", max_length=200, default=0)
    extra = models.FloatField(u"extra", default=0)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        del dicts["id"]
        return dicts

class Equip(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"装备"
    name = models.CharField(u"名字", max_length=200, default="")
    attrList_int = models.CharField(u"属性配置", max_length=200)
    decomposeRefinePoint = models.IntegerField(u"分解获取精炼点", default=0)
    icon = models.CharField(u"图标对应的图片名字", max_length=200)
    descriptionId = models.CharField(u"信息描述", max_length=200)
    nameId = models.CharField(u"名称id", max_length=200)
    powerRankBase = models.IntegerField(u"基础战斗力，用来计算装备分数的")
    powerRankIncrease = models.IntegerField(u"每一级增长的战斗力，用来计算装备分数（与等级相关）")
    quality = models.IntegerField(u"品质")
    category = models.IntegerField(u"装备部位：1武器，2衣服，3头盔，4装饰")
    heroTypeList_int = models.CharField(u"装备的英雄的类型", max_length=200)
    searchDifficuty_int = models.CharField(u"出处所在关卡的难度", max_length=200, default=0)
    searchInstances_int = models.CharField(u"出处所在关卡id", max_length=200, default=0)
    equipSuitId = models.IntegerField(u"套装ID", default=0)

    def __unicode__(self):
        return u"%s:%s" %(self.pk, self.nameId)

    class Meta:
        ordering = ["id"]

    #@property
    #def is_white(self):
    #    return self.quality == 1

    @property
    def is_green(self):
        return self.quality == 2

    @property
    def is_blue(self):
        return self.quality == 3

    @property
    def is_purple(self):
        return self.quality == 4

    @property
    def is_orange(self):
        return self.quality == 5

    def can_wear(self, pos):
        return self.category == pos 

    @property
    def heroTypeList(self):
        return  [int(float(i)) for i in self.heroTypeList_int.strip().split(",") if i]

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["attrList"] = [_equipattr.to_dict() for _equipattr in self.attrList]
        dicts["pk"] = dicts["id"]
        del dicts["id"]
        return dicts

    @memoized_property
    def attrList(self):
        if self.attrList_int.strip():
            return [EquipAttribute.get(float(pk)) for pk in self.attrList_int.strip().split(",") if pk]
        return []

class EquipEnhance(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"装备强化"
    gold = models.IntegerField(u"enhanceGold")
    
    class Meta:
        ordering = ["id"]

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        del dicts["id"]
        dicts["level"] = self.pk
        return dicts

class EquipAttribute(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"装备属性"
    id = models.BigIntegerField(u"主键",primary_key = True)
    attrType = models.CharField(u"attrType", max_length=200)
    enhanceInitValue = models.FloatField(u"强化初始值", default=0)
    enhanceAttrGrowth = models.FloatField(u"强化成长加值", default=0)
    refineInitValue = models.FloatField(u"精炼初始值", default=0)
    refineAttrGrowth = models.FloatField(u"精炼成长加值", default=0)

    class Meta:
        ordering = ["id"]

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        del dicts["id"]
        return dicts

class EquipRefine(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"装备精炼"
    quality = models.IntegerField(u"分类")
    refineLevel = models.IntegerField(u"精炼等级", default=0)
    equipLevel = models.IntegerField(u"装备等级", default=1)
    refineXp = models.IntegerField(u"精炼消耗")

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = dicts["id"]
        del dicts["id"]
        return dicts

class EquipFragment(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"装备碎片"
    name = models.CharField(u"name", max_length=200, default=0)
    equipId = models.IntegerField(u"合成后的装备", default=0)
    nameId = models.CharField(u"nameId", max_length=200, default="")
    composeCount = models.IntegerField(u"合成数量", default=0)
    descriptionId = models.CharField(u"info", max_length=200, default="")
    searchDifficuty_int = models.CharField(u"出处所在关卡的难度", max_length=200, default=0)
    searchInstances_int = models.CharField(u"出处所在关卡id", max_length=200, default=0)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = self.pk
        del dicts["id"]
        del dicts["name"]
        return dicts

    @memoized_property
    def equip(self):
        return Equip.get(self.equipId)

    @property
    def quality(self):
        return self.equip.quality
