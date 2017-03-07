# -*- coding: utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler
from module.common.static import Static

class Icon(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"头像"
    iconId = models.CharField(u"iconID", max_length=50, default="")

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["gid"] = self.pk
        del dicts["id"]
        return dicts
