# -*- coding: utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler
from common.decorators.memoized_property import memoized_property

class Tutorial(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"新手引导"
    nameId = models.CharField(u'名称', max_length=50, default="")
    icon = models.CharField(u'图标', max_length=50, default="")
    level = models.IntegerField(u'level', default=0)
    descriptionId = models.CharField(u'pop text', max_length=200, default="")
    preGid = models.IntegerField(u'pre gid', default=0)

    class Meta:
        verbose_name = u'新手引导'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return u'%s' % (self.nameId)
    
    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = self.preGid
        del dicts["id"]
        del dicts["preGid"]
        return dicts

class TutorialDetail(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"新手引导详细"
    guideGid = models.IntegerField(u'guideGid', default=0)
    scenarioId = models.IntegerField(u'scenarioId', default=0)
    step = models.IntegerField(u'step', default=0)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        del dicts["id"]
        return dicts

class Plot(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"剧情"
    gid = models.IntegerField(u'pk', default=0)
    roleId = models.IntegerField(u'roleId', default=0)
    serialIndex = models.IntegerField(u'serialIndex', default=0)
    speakerType = models.IntegerField(u'speakerType', default=0)
    dialogId = models.CharField(u'dialogId', max_length=200, default="")
    animationType = models.IntegerField(u'animationType', default=0) 

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = self.gid
        del dicts["id"]
        return dicts
