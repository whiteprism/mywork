# -*- coding: utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler
from common.decorators.memoized_property import memoized_property

class Artifact(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"圣物"
    name = models.CharField(u"name", max_length=200, default=0)
    upgradeXp = models.IntegerField(u"强化时提供基础经验", default=0)
    icon = models.CharField(u"icon", max_length=200, default="")
    descriptionId = models.CharField(u"descriptionId", max_length=200, default="")
    nameId = models.CharField(u"nameId", max_length=200, default="")
    quality = models.IntegerField(u"品质", default=0)
    orderId = models.IntegerField(u"显示顺序", default=0)
    # composeFragmentIds_int = models.CharField(u"圣物碎片ID", max_length=200, default="")
    category = models.IntegerField(u"category", default=0)
    skillIds_int = models.CharField(u"随机技能列表", max_length=200, default=0)
    attrList_int = models.CharField(u"属性配置", max_length=200, default=0)
    # heroTypeList_int = models.CharField(u"装备的英雄的类型", max_length=200, default="")

    # @memoized_property
    # def composeFragments(self):
    #     return [ArtifactFragment.get(i) for i in self.fragment_ids]

    # @memoized_property
    # def fragment_ids(self):
    #     return [int(float(i)) for i in self.composeFragmentIds_int.strip().split(",") if i]

    # @memoized_property
    # def heroTypeList(self):
    #     return  [int(float(i)) for i in self.heroTypeList_int.strip().split(",") if i]

    # @property
    # def is_white(self):
    #     """
    #     白色
    #     """
    #     return self.quality == 1

    # @property
    # def is_green(self):
    #     """
    #     绿色
    #     """
    #     return self.quality == 2

    @property
    def is_blue(self):
        """
        蓝色
        """
        return self.quality == 3

    @property
    def is_purple(self):
        """
        紫色
        """
        return self.quality == 4

    @property
    def is_orange(self):
        """
        橙色
        """
        return self.quality == 5

    def can_wear(self, pos):
        return self.category == pos

    @property
    def skillIds(self):
        if self.skillIds_int.strip():
            skills = [int(float(skillId)) for skillId in self.skillIds_int.strip().split(",") if skillId]
            return zip(skills[0::2], skills[1::2])
        return []

    @memoized_property
    def attrList(self):
        if self.attrList_int.strip():
            return [ArtifactAttribute.get(int(float(pk))) for pk in self.attrList_int.strip().split(",") if pk]
        return []

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = self.pk
        dicts["attrList"] = [_attr.to_dict() for _attr in self.attrList]
        del dicts["id"]
        del dicts["name"]
        return dicts

class ArtifactEnhance(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"圣物强化"
    xp = models.IntegerField(u"enhanceXp")
    quality = models.IntegerField(u"分类")
    level = models.IntegerField(u"level")
    playerLevel = models.IntegerField(u"玩家等级", default=1)

    class Meta:
        ordering = ["id"]

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = self.pk
        del dicts["id"]
        return dicts

class ArtifactAttribute(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"圣物属性"
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

# class ArtifactFragmentGrabProb(models.Model, StaticDataRedisHandler, CommonStaticModels):
#     SHEET_NAME = u"圣物碎片抢夺概率"
#     robotProb = models.IntegerField(u"机器人单次抢夺概率", default=0)
#     playerProb = models.IntegerField(u"真人单次抢夺概率", default=0)
#     robotTenProbs_int = models.CharField(u"机器人10次抢夺概率", max_length=200, default="")

#     @memoized_property
#     def robotTenProbs(self):
#         data = [int(float(i)) for i in self.robotTenProbs_int.strip().split(",") if i]
#         probs = []
#         for i, prob in enumerate(data):
#             probs.append((i+1, prob))

#         return probs

#     def grab_prob(self, is_robot=True):
#         if is_robot:
#             prob = self.robotProb
#         else:
#             prob = self.playerProb

#         if prob >= 75:
#             return 1
#         elif prob >= 50:
#             return 2
#         elif prob >= 25:
#             return 3
#         else:
#             return 4

class ArtifactFragment(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"圣物碎片"
    name = models.CharField(u"name", max_length=200, default=0)
    artifactId = models.IntegerField(u"合成后圣物ID", default=0)
    nameId = models.CharField(u"nameId", max_length=200, default="")
    icon = models.CharField(u"icon", max_length=200, default="")
    descriptionId = models.CharField(u"descriptionId", max_length=200, default="")
    # pos = models.IntegerField(u"碎片部位ID", default=0)
    composeCount = models.IntegerField(u"合成数量", default=0)
    searchDifficuty_int = models.CharField(u"掉落关卡难度", max_length=200, default="")
    searchInstances_int = models.CharField(u"掉落关卡", max_length=200, default="")

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["gid"] = self.pk

        del dicts["id"]
        del dicts["name"]
        return dicts

    @memoized_property
    def artifact(self):
        return Artifact.get(self.artifactId)

    @property
    def quality(self):
        return self.artifact.quality


class ArtifactRefine(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"圣物精炼"
    quality = models.IntegerField(u"分类")
    refineLevel = models.IntegerField(u"精炼等级", default=0)
    playerLevel = models.IntegerField(u"需要玩家等级")
    refineCost = models.IntegerField(u"精炼消耗")
    # artifactCount = models.IntegerField(u"需要消耗同样圣物的数量", default=0)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = dicts["id"]
        del dicts["id"]
        return dicts
