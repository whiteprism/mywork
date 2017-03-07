# -*- coding: utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
import datetime
from submodule.fanyoy.redis import StaticDataRedisHandler
from module.common.decorators.memoized_property import memoized_property

class Experiment(models.Model, StaticDataRedisHandler, CommonStaticModels):
    """
    实验
    """
    id = models.CharField("实验名称", max_length=100, primary_key=True)
    valuesStr = models.TextField("附加值", help_text="根据实验使用环境定义DEMO:a:1,2,3[回车][回车]b:1", blank=True)
    whitelist = models.TextField("白名单", help_text="此白名单为附加白名单", blank=True)
    blacklist = models.TextField("黑名单", help_text="此黑名单为附加黑名单", blank=True)
    is_alltime = models.BooleanField("时间段检查", default=False)
    started_at = models.DateTimeField(u"开始时间", default=datetime.datetime(2000,1,1,0,0,0)) #开始时间
    ended_at = models.DateTimeField(u"结束时间", default=datetime.datetime(2000,1,1,0,0,0))  #结束时间
    is_weektime = models.BooleanField("星期点检查", default=False)
    weekdays_str = models.TextField("星期", help_text="以半角,分割", blank=True)
    week_started_at = models.TimeField(u"每周几开始时间", default=datetime.time(0,0,0)) #开始时间
    week_ended_at = models.TimeField(u"每周几结束时间", default=datetime.time(0,0,0))  #结束时间

    def __unicode__(self):
        return "Experiment::%s" % self.name

    class Meta:
        verbose_name = u'实验'
        verbose_name_plural = verbose_name


    @memoized_property
    def values(self):
        values = {}
        if self.valuesStr:
            valueTs = self.valuesStr.split("\r\n\r\n")
            for valueT in valueTs:
                if valueT.strip():
                    k, v = valueT.strip().split(":")
                    if "," in v:
                        v = [i.strip() for i in v.split(",") if i.strip()]
                    values[k.strip()] = v
        return values

    @property
    def weekdays(self):
        return [int(float(w)) for w in self.weekdays_str.strip().split(",") if w]

    def save(self, *args, **kwargs):
        super(Experiment, self).save(*args, **kwargs)
        Experiment.create_cache()

    def delete(self, *args, **kwargs):
        super(Experiment, self).delete(*args, **kwargs)
        Experiment.create_cache()

    @property
    def name(self):
        return self.id

    @memoized_property
    def whites(self):
        '''
        白名单
        '''
        whites = []
        whiteStr = self.whitelist.strip()

        if not whiteStr:
            return whites
        
        listdata = whiteStr.split(",")

        for pid in listdata:
            try:
                pid = int(pid)
                whites.append(pid)
            except:
                continue
        
        return whites

    @memoized_property
    def blacks(self):
        '''
        黑名单  
        '''
        blacks = []
        blackStr = self.blacklist.strip()

        if not blackStr:
            return blacks
        
        listdata = blackStr.split(",")

        for pid in listdata:
            try:
                pid = int(pid)
                blacks.append(pid)
            except:
                continue
        
        return blacks
