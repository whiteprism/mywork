# -*- coding:utf-8 -*-
from django.db import models

class ServerInfo(models.Model):
    id = models.IntegerField(u"服务器ID", primary_key=True)
    code = models.CharField(u"服务器代号",max_length=30,default="")
    zone_id = models.IntegerField(u"区域ID",default=1)
    zone_name = models.CharField(u"区域名称", max_length=30)
    name = models.CharField(u"服务器名称", max_length=20, unique=True)
    url = models.CharField(u"连接地址", max_length=200, blank=True, null=True)
    status_id = models.IntegerField(u"服务器状态ID", default=1)
    status_text = models.CharField(u"服务器状态描述", max_length=20)
    open_at = models.CharField(u"开服时间", max_length=200)
    gm_url = models.CharField(u"连接地址", max_length=200, blank=True, null=True)

    class Meta:
        ordering = ["id"]
