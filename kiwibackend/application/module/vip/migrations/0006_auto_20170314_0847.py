# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vip', '0005_auto_20170119_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='vip',
            name='fortCount',
            field=models.IntegerField(default=0, verbose_name='\u5821\u5792\u6570\u91cf'),
        ),
        migrations.AddField(
            model_name='vip',
            name='fortTime',
            field=models.IntegerField(default=0, verbose_name='\u5821\u5792CD'),
        ),
        migrations.AddField(
            model_name='vip',
            name='resetCost',
            field=models.IntegerField(default=0, verbose_name='\u51b7\u5374\u5821\u5792\u6d88\u8017'),
        ),
        migrations.AddField(
            model_name='vip',
            name='safeTime',
            field=models.IntegerField(default=0, verbose_name='\u4fdd\u62a4\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='vip',
            name='transitCount',
            field=models.IntegerField(default=0, verbose_name='\u8fd0\u8f93\u6570\u91cf'),
        ),
        migrations.AddField(
            model_name='vip',
            name='transitTime',
            field=models.IntegerField(default=0, verbose_name='\u8fd0\u8f93\u65f6\u95f4'),
        ),
    ]
