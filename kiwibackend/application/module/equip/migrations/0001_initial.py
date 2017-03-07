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
            name='CardEquipInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pos1_int', models.CharField(max_length=300, verbose_name='\u4f4d\u7f6e1')),
                ('pos2_int', models.CharField(max_length=300, verbose_name='\u4f4d\u7f6e2')),
                ('pos3_int', models.CharField(max_length=300, verbose_name='\u4f4d\u7f6e3')),
                ('pos4_int', models.CharField(max_length=300, verbose_name='\u4f4d\u7f6e4')),
                ('pos5_int', models.CharField(max_length=300, verbose_name='\u4f4d\u7f6e5')),
                ('pos6_int', models.CharField(max_length=300, verbose_name='\u4f4d\u7f6e6')),
                ('pos7_int', models.CharField(max_length=300, verbose_name='\u4f4d\u7f6e7')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='Equip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=200, verbose_name='\u540d\u5b57')),
                ('attrList_int', models.CharField(max_length=200, verbose_name='\u5c5e\u6027\u914d\u7f6e')),
                ('decomposeCost', models.IntegerField(verbose_name='\u5206\u89e3\u82b1\u8d39')),
                ('gradePlus', models.IntegerField(verbose_name='\u8363\u8a89\u7b49\u7ea7\u663e\u793a=\u88c5\u5907\u540d\u5b57+\u8be5\u7b49\u7ea7')),
                ('gemSlots', models.IntegerField(verbose_name='\u5b9d\u77f3\u69fd\u4f4d\uff0c\u80fd\u9576\u5d4c\u51e0\u4e2a\u5b9d\u77f3')),
                ('icon', models.CharField(max_length=200, verbose_name='\u56fe\u6807\u5bf9\u5e94\u7684\u56fe\u7247\u540d\u5b57')),
                ('descriptionId', models.CharField(max_length=200, verbose_name='\u4fe1\u606f\u63cf\u8ff0')),
                ('nameId', models.CharField(max_length=200, verbose_name='\u540d\u79f0id')),
                ('powerRankBase', models.IntegerField(verbose_name='\u57fa\u7840\u6218\u6597\u529b\uff0c\u7528\u6765\u8ba1\u7b97\u88c5\u5907\u5206\u6570\u7684')),
                ('powerRankIncrease', models.IntegerField(verbose_name='\u6bcf\u4e00\u7ea7\u589e\u957f\u7684\u6218\u6597\u529b\uff0c\u7528\u6765\u8ba1\u7b97\u88c5\u5907\u5206\u6570\uff08\u4e0e\u7b49\u7ea7\u76f8\u5173\uff09')),
                ('upgradeAttrList_int', models.CharField(max_length=200, verbose_name='\u5c5e\u6027\u589e\u957f\u503c')),
                ('upgradeEquipId', models.IntegerField(default=0, verbose_name='\u8fdb\u5316\u6210\u65b0\u6b66\u5668\u7684id')),
                ('quality', models.IntegerField(verbose_name='\u54c1\u8d28')),
                ('upgrade', models.IntegerField(default=0, verbose_name='\u8fdb\u9636\u72b6\u6001')),
                ('category', models.IntegerField(verbose_name='\u88c5\u5907\u90e8\u4f4d\uff1a1\u6b66\u5668\uff0c2\u8863\u670d\uff0c3\u5934\u76d4\uff0c4\u88c5\u9970')),
                ('heroTypeList_int', models.CharField(max_length=200, verbose_name='\u88c5\u5907\u7684\u82f1\u96c4\u7684\u7c7b\u578b')),
                ('gemList_int', models.CharField(max_length=200, verbose_name='\u8fdb\u9636\u6750\u6599')),
                ('gemAttrList_float', models.CharField(max_length=200, verbose_name='\u8fdb\u9636\u5c5e\u6027')),
                ('searchDifficuty_int', models.CharField(default=0, max_length=200, verbose_name='\u51fa\u5904\u6240\u5728\u5173\u5361\u7684\u96be\u5ea6')),
                ('searchInstances_int', models.CharField(default=0, max_length=200, verbose_name='\u51fa\u5904\u6240\u5728\u5173\u5361id')),
                ('unBindCostDiamond', models.IntegerField(default=0, verbose_name='\u89e3\u9664\u7ed1\u5b9a\u8017\u8d39\u94bb\u77f3')),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='EquipAttribute',
            fields=[
                ('id', models.BigIntegerField(serialize=False, verbose_name='\u4e3b\u952e', primary_key=True)),
                ('attrGrowth', models.FloatField(verbose_name='\u6210\u957f\u52a0\u503c')),
                ('attrType', models.CharField(max_length=200, verbose_name='attrType')),
                ('initValue', models.FloatField(verbose_name='\u521d\u59cb\u503c')),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='EquipEnhance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gold', models.IntegerField(verbose_name='enhanceGold')),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='EquipFragment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=0, max_length=200, verbose_name='name')),
                ('equipId', models.IntegerField(default=0, verbose_name='\u5408\u6210\u540e\u7684\u88c5\u5907')),
                ('nameId', models.CharField(default=b'', max_length=200, verbose_name='nameId')),
                ('composeCount', models.IntegerField(default=0, verbose_name='\u5408\u6210\u6570\u91cf')),
                ('descriptionId', models.CharField(default=b'', max_length=200, verbose_name='info')),
                ('searchDifficuty_int', models.CharField(default=0, max_length=200, verbose_name='\u51fa\u5904\u6240\u5728\u5173\u5361\u7684\u96be\u5ea6')),
                ('searchInstances_int', models.CharField(default=0, max_length=200, verbose_name='\u51fa\u5904\u6240\u5728\u5173\u5361id')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
    ]
