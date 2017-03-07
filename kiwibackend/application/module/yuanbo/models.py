# -*- coding: utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler
from common.decorators.memoized_property import memoized_property

class Yuanbo(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"钻石商店"
    name = models.CharField(u'名称', max_length=50, default="")
    iconId = models.CharField(u'名称', max_length=50, default="")
    price = models.IntegerField(u'平台价格', default=0)
    amount = models.IntegerField(u'购买元宝数量', default=0)
    first_amount = models.IntegerField(u'奖励元宝数量', default=0)
    reward_amount = models.IntegerField(u'奖励元宝数量', default=0)
    is_ios = models.BooleanField(default = False)

    class Meta:
        verbose_name = u'元宝数据'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return u'%s' % (self.name)
