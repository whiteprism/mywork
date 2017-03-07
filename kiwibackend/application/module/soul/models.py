# -*- coding: utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler

class Soul(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"灵魂碎片"
    warrior_id = models.IntegerField(u"英雄id")
    name = models.CharField(u"碎片名称",  max_length=200)
    couragePoint = models.IntegerField(u"一个灵魂碎片对应的N个徽章")
    descriptionId = models.CharField(u"", default="", max_length=200)
    searchDifficuty_int = models.CharField(u"该魂魄在哪里掉落那里的难度", default="", max_length=200)
    searchInstances_int = models.CharField(u"该魂魄在哪些关卡会掉落", default="", max_length=200)
    gold = models.IntegerField(u"一个灵魂碎片对应分解出来的钱数")
    icon = models.CharField(u"icon", max_length=200)
    nameId = models.CharField(u"nameId", max_length=200)
    quality = models.IntegerField(u"次组配置中，该灵魂碎片的个数")
    recruitCost = models.IntegerField(u"合成目标英雄的价格")
    breakCost = models.IntegerField(u"获得英雄分解获得灵魂碎片个数")
    recruitHeroId = models.IntegerField(u"谁的灵魂碎片")

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["gid"] = self.pk
        del dicts["id"]
        del dicts["name"]
        return dicts

    @property
    def is_soul(self):
        return True
