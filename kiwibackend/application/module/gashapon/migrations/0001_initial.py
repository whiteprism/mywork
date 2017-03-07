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
            name='Gashapon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=200, verbose_name='\u62bd\u5956\u540d\u79f0')),
                ('topreward_number', models.SmallIntegerField(default=0, verbose_name='n\u6b21\u5fc5\u51fa')),
                ('topreward_rarity', models.SmallIntegerField(default=0, verbose_name='\u5fc5\u51fa\u5206\u7c7b')),
                ('topreward_quality', models.SmallIntegerField(default=0, verbose_name='\u5fc5\u51fa\u7a00\u6709\u5ea6')),
                ('topreward_reset', models.BooleanField(default=False, verbose_name='\u5fc5\u51fa\u540e\u662f\u5426\u91cd\u7f6e')),
                ('description', models.CharField(default=b'', max_length=200, verbose_name='\u63cf\u8ff0')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='GashaponProbability',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rarity', models.SmallIntegerField(verbose_name='\u7a00\u6709\u5ea6')),
                ('target_id', models.IntegerField(verbose_name='\u5956\u54c1')),
                ('probability', models.IntegerField(verbose_name='\u6982\u7387')),
                ('number', models.IntegerField(default=0, verbose_name='\u6570\u91cf')),
                ('gashapon', models.ForeignKey(to='gashapon.Gashapon')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='GashaponRarityProbability',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quality', models.SmallIntegerField(default=0, verbose_name='\u661f\u7ea7')),
                ('rarity', models.SmallIntegerField(default=1, verbose_name='\u7a00\u6709\u5ea6')),
                ('probability', models.IntegerField(default=0, verbose_name='\u6982\u7387')),
                ('gashapon', models.ForeignKey(to='gashapon.Gashapon')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='Tavern',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cdTime', models.IntegerField(default=0, verbose_name='cdTime')),
                ('level', models.IntegerField(default=0, verbose_name='level')),
                ('cost', models.IntegerField(default=0, verbose_name='cost')),
                ('maxDailyCount', models.IntegerField(default=0, verbose_name='\u6bcf\u65e5\u514d\u8d39\u6b21\u6570')),
                ('tenCost', models.IntegerField(default=0, verbose_name='\u5341\u8fde\u62bd')),
                ('discount', models.IntegerField(default=0, verbose_name='\u6298\u6263')),
                ('gashapon_id', models.IntegerField(default=0, verbose_name='\u5bf9\u5e94\u62bd\u5956ID')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='TavernCost',
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
