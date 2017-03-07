# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0002_auto_20150908_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemcompose',
            name='orderId',
            field=models.IntegerField(default=0, verbose_name='id\u524d\u7aef\u5206\u9875'),
        ),
        migrations.AddField(
            model_name='itemcompose',
            name='type',
            field=models.IntegerField(default=0, verbose_name='\u7c7b\u578b\u524d\u7aef\u5206\u9875'),
        ),
    ]
