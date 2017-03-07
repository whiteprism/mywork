# -*- coding:utf-8 -*-
from django.db import models

class UserFeedback(models.Model):
    name = models.CharField(default="", max_length=200)
    email = models.EmailField()
    message = models.TextField(default="", max_length=2000)
    send_time = models.DateTimeField()
    response_flag = models.BooleanField(default=False)
