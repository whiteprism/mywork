# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0004_auto_20170104_1036'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attrType', models.CharField(max_length=200, verbose_name='attrType')),
                ('minValue', models.IntegerField(default=0, verbose_name='\u6700\u5c0f\u503c')),
                ('maxValue', models.IntegerField(default=0, verbose_name='\u6700\u5927\u503c')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='BuildingFragment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=0, max_length=200, verbose_name='name')),
                ('buildingId', models.IntegerField(default=0, verbose_name='\u5408\u6210\u540e\u5efa\u7b51ID')),
                ('nameId', models.CharField(default=b'', max_length=200, verbose_name='nameId')),
                ('icon', models.CharField(default=b'', max_length=200, verbose_name='icon')),
                ('descriptionId', models.CharField(default=b'', max_length=200, verbose_name='descriptionId')),
                ('composeCount', models.IntegerField(default=0, verbose_name='\u5408\u6210\u6570\u91cf')),
                ('searchDifficuty_int', models.CharField(default=b'', max_length=200, verbose_name='\u6389\u843d\u5173\u5361\u96be\u5ea6')),
                ('searchInstances_int', models.CharField(default=b'', max_length=200, verbose_name='\u6389\u843d\u5173\u5361')),
                ('removeRewardIds_str', models.CharField(default=0, max_length=200, verbose_name='\u8fd4\u8fd8\u6570\u91cf')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.AddField(
            model_name='building',
            name='attrList_int',
            field=models.CharField(default=b'', max_length=100, verbose_name='\u5c5e\u6027\u914d\u7f6e'),
        ),
    ]
