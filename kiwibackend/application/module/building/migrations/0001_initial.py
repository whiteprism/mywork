# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=200, verbose_name='name')),
                ('nameId', models.CharField(default=b'', max_length=200, verbose_name='nameId')),
                ('buildCamera', models.IntegerField(default=0, verbose_name='\u5efa\u9020\u65f6\u662f\u5426\u5bf9\u51c6')),
                ('buildingToastId', models.CharField(default=b'', max_length=200, verbose_name='\u73a9\u5bb6\u7b49\u7ea7\u672a\u8fbe\u5230\u65f6\u7684\u63d0\u793a\u4fe1\u606f')),
                ('category', models.IntegerField(default=0, verbose_name='\u5efa\u7b51\u79cd\u7c7b')),
                ('descriptionId', models.CharField(default=b'', max_length=200, verbose_name='desc')),
                ('orderId', models.IntegerField(default=0, verbose_name='\u6392\u5e8f')),
                ('width', models.IntegerField(default=0, verbose_name='\u5bbd\u5ea6')),
                ('height', models.IntegerField(default=0, verbose_name='\u9ad8\u5ea6')),
                ('model', models.CharField(default=b'', max_length=200, verbose_name='\u6a21\u578b')),
                ('summaryId', models.CharField(default=b'', max_length=200, verbose_name='summaryId')),
                ('buildingToWarriorId', models.IntegerField(default=0, verbose_name='\u5efa\u7b51\u5bf9\u5e94\u7684\u5c0f\u5175Id')),
                ('levelCount_int', models.CharField(default=b'', max_length=200, verbose_name='\u5947\u6570\u4f4d\u7b49\u7ea7\uff0c\u5076\u6570\u4f4d\u6570\u91cf')),
                ('unlockUserLevel', models.IntegerField(default=0, verbose_name='\u73a9\u5bb6\u89e3\u9501\u7b49\u7ea7')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='BuildingGolden',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.IntegerField(default=0, verbose_name='\u7b49\u7ea7')),
                ('minHarvestScale', models.IntegerField(default=0, verbose_name='\u53ef\u4ee5\u6267\u884c\u91c7\u96c6\u6240\u9700\u7684\u6700\u5c0f\u6570\u91cf')),
                ('productionPerHour', models.IntegerField(default=0, verbose_name='\u6bcf\u5c0f\u65f6\u4ea7\u91cf')),
                ('storage', models.IntegerField(default=0, verbose_name='\u6700\u5927\u5b58\u91cf')),
                ('building', models.ForeignKey(to='building.Building')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='BuildingProduction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buildingLevel', models.IntegerField(default=0, verbose_name='\u7b49\u7ea7')),
                ('cost_int', models.CharField(default=b'', max_length=200, verbose_name='\u6d88\u8017')),
                ('productionId', models.IntegerField(default=0, verbose_name='\u4ea7\u7269ID')),
                ('productionLevel', models.IntegerField(default=0, verbose_name='\u4ea7\u7269\u7b49\u7ea7')),
                ('productionType', models.IntegerField(default=0, verbose_name='\u4ea7\u7269\u7c7b\u578b')),
                ('useTime', models.IntegerField(default=0, verbose_name='\u6d88\u8017\u65f6\u95f4')),
                ('building', models.ForeignKey(to='building.Building')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='BuildingProductionCost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField(default=0, verbose_name='count')),
                ('level', models.IntegerField(default=0, verbose_name='level')),
                ('type', models.IntegerField(default=0, verbose_name='type')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='BuildingResourceProtected',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('building', models.IntegerField(default=0, verbose_name='\u5efa\u7b51id')),
                ('level', models.IntegerField(default=0, verbose_name='\u7b49\u7ea7')),
                ('goldCount', models.IntegerField(default=0, verbose_name='\u4fdd\u62a4\u91d1\u5e01\u6570\u91cf')),
                ('woodCount', models.IntegerField(default=0, verbose_name='\u4fdd\u62a4\u6728\u5934\u6570\u91cf')),
                ('percentage', models.FloatField(default=0, verbose_name='\u4fdd\u62a4\u6570\u91cf\u767e\u5206\u6bd4')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='BuildingUpgrade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('costs_int', models.CharField(default=b'', max_length=200, verbose_name='\u6d88\u8017')),
                ('level', models.IntegerField(default=0, verbose_name='\u7b49\u7ea7')),
                ('castleLevel', models.IntegerField(default=0, verbose_name='\u4e3b\u57ce\u7b49\u7ea7')),
                ('userLevel', models.IntegerField(default=0, verbose_name='\u7528\u6237\u7b49\u7ea7')),
                ('useTime', models.IntegerField(default=0, verbose_name='\u82b1\u8d39\u65f6\u95f4')),
                ('building', models.ForeignKey(to='building.Building')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='BuildingUpgradeCost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField(default=0, verbose_name='count')),
                ('level', models.IntegerField(default=0, verbose_name='level')),
                ('type', models.IntegerField(default=0, verbose_name='type')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
    ]
