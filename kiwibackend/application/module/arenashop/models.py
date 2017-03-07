# -*- coding: utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler
from common.decorators.memoized_property import memoized_property
from module.common.static import Static

class ArenaShop(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"荣誉商店"
    name = models.CharField(u"名字", max_length=50)
    itemId = models.IntegerField(u"gid",default=0)
    count = models.IntegerField(u"count",default=0)
    #itemLevel = models.IntegerField(u"level",default=0)
    score = models.IntegerField(u"score",default=0)
    category = models.IntegerField(u"分类",default=0)
    probability = models.IntegerField(u"概率",default=0)
    type = models.IntegerField(u"显示类别",default=0)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()

        dicts["pk"] = dicts["id"] 
        del dicts["id"]
        del dicts["name"]

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
