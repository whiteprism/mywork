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
            name='LevelConf',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('battleLeftDownX', models.IntegerField(default=0, verbose_name='\u5f00\u683c\u5b50')),
                ('battleLeftDownY', models.IntegerField(default=0, verbose_name='\u5f00\u683c\u5b50')),
                ('battleRightTopX', models.IntegerField(default=0, verbose_name='\u5f00\u683c\u5b50')),
                ('battleRightTopY', models.IntegerField(default=0, verbose_name='\u5f00\u683c\u5b50')),
                ('energy', models.IntegerField(default=0, verbose_name='\u4f53\u529b')),
                ('heroUpgradeLimit', models.IntegerField(default=0, verbose_name='\u82f1\u96c4\u8fdb\u9636\u9650\u5236')),
                ('levelUpRewards_int', models.CharField(default=b'', max_length=200, verbose_name='\u5347\u7ea7\u5956\u52b1\u5217\u8868')),
                ('rewardPower', models.IntegerField(default=0, verbose_name='\u5956\u52b1\u4f53\u529b')),
                ('rewardStamina', models.IntegerField(default=0, verbose_name='\u5956\u52b1\u7684\u8010\u529b')),
                ('stamina', models.IntegerField(default=0, verbose_name='\u8010\u529b')),
                ('wallHp', models.IntegerField(default=0, verbose_name='\u5899\u8840')),
                ('xp', models.IntegerField(default=0, verbose_name='\u7ecf\u9a8c\u4e0a\u9650')),
                ('unlockIconId', models.IntegerField(default=0, verbose_name='\u89e3\u9501ICON')),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='LevelUpReward',
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
