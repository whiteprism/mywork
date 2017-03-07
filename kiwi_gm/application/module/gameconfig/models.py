# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from common.decorators.memoized_property import memoized_property

SECRET_LEVELS = (
    (1, u"普通A"),
    (2, u"普通B"),
    (3, u"普通C"),
    (4, u"特殊A"),
    (5, u"特殊B"),
    (6, u"特殊C"),
)

class GameModel(models.Model):
    name = models.CharField(u"模块名称", max_length=20, unique=True)
    url = models.CharField(u"连接地址", max_length=100, blank=True, null=True)
    sort = models.IntegerField(u"排序", default = 1)
    secret_level= models.IntegerField(u"授权等级", default = 1, choices=SECRET_LEVELS)
    tag = models.CharField(u"模块tag", max_length=20)

    class Meta:
        verbose_name = u'模块'
        default_related_name = verbose_name
        verbose_name_plural = verbose_name
        ordering = ["sort"]

    def __unicode__(self):
        return u'%s' % (self.name)


class GameFunc(models.Model):
    name = models.CharField(u"名称", max_length=20, unique=True)
    gamemodel = models.ManyToManyField(GameModel, verbose_name=u"模块")
    url = models.CharField(u"连接地址", max_length=100, blank=True, null=True)
    sort = models.IntegerField(u"排序", default = 1)
    secret_level= models.IntegerField(u"授权等级", default = 1, choices=SECRET_LEVELS)

    class Meta:
        verbose_name = u'功能'
        default_related_name = verbose_name
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return u'%s' % (self.name)


class GameAuth(models.Model):
    user = models.ForeignKey(User, verbose_name=u"用户")
    secret_level= models.IntegerField(u"授权等级", default = 1, choices=SECRET_LEVELS)
    def __unicode__(self):
        return u'%s' % (self.user)

    class Meta:
        verbose_name = u'用户权限'
        verbose_name_plural = verbose_name
