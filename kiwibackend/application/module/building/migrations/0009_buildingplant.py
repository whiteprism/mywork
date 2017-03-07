# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0008_auto_20170105_1722'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingPlant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buildingId', models.IntegerField(default=0, verbose_name='\u690d\u7269ID')),
                ('seedId', models.IntegerField(default=0, verbose_name='\u79cd\u5b50ID')),
                ('harvestId', models.IntegerField(default=0, verbose_name='\u4ea7\u7269ID')),
                ('output', models.IntegerField(default=0, verbose_name='\u4ea7\u91cf')),
                ('harvestTimes', models.IntegerField(default=0, verbose_name='\u53ef\u91c7\u6458\u7684\u6b21\u6570')),
                ('harvestInterval', models.IntegerField(default=0, verbose_name='\u91c7\u6458\u7684\u65f6\u95f4\u95f4\u9694')),
                ('growthInterval', models.IntegerField(default=0, verbose_name='\u5e7c\u82d7\u5230\u6210\u957f\u65f6\u95f4\u95f4\u9694')),
                ('matureInterval', models.IntegerField(default=0, verbose_name='\u6210\u957f\u5230\u6210\u719f\u65f6\u95f4\u95f4\u9694')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
    ]