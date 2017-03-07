# -*- coding: utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler

class Attr(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"属性UI说明"
    attr = models.CharField(u"属性", max_length=200)
    nameId = models.CharField(u"多语言", max_length=200)
    enumId = models.IntegerField(u"枚举ID",default=0)

    def __unicode__(self):
        return u"%s:%s:%s" %(self.pk, self.attr, self.nameId)


    def to_dict(self):
        dicts = super(Attr, self).to_dict()
        dicts["pk"] = self.enumId
        del dicts["id"]
        return dicts
