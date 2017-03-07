# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_sevendaystask'),
    ]

    operations = [
        migrations.AddField(
            model_name='sevendaystask',
            name='pageId',
            field=models.IntegerField(default=0, verbose_name='\u9875\u7801'),
        ),
        migrations.AddField(
            model_name='sevendaystask',
            name='type',
            field=models.IntegerField(default=0, verbose_name='\u7c7b\u578b'),
        ),
    ]
