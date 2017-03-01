# -*- coding:utf-8 -*-
from django.db import models
from datetime import datetime
import django.utils.timezone as timezone

# Create your models here.
class blogPost(models.Model):
    title = models.CharField(u"标题", max_length=30)
    content = models.TextField(u"内容",default="", max_length=3000)
    time = models.DateTimeField(u"时间",default=timezone.now)

    class Meta:
        verbose_name = u'博客'
        default_related_name = verbose_name
        verbose_name_plural = verbose_name
        ordering = ["-time"]
