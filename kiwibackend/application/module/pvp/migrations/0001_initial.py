# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PVPRank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=40, verbose_name='\u540d\u79f0')),
                ('titleID', models.CharField(default=b'', max_length=200, verbose_name='ID')),
                ('score', models.IntegerField(default=0, verbose_name='\u79ef\u5206')),
                ('rank', models.IntegerField(default=0, verbose_name='\u6392\u540d')),
                ('weeklyRewards_int', models.CharField(default=b'', max_length=200, verbose_name='\u5956\u52b1')),
                ('dailyRewards_int', models.CharField(default=b'', max_length=200, verbose_name='\u6bcf\u65e5\u6392\u884c\u5956\u52b1')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='PVPReward',
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
            name='PVPScene',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('scene', models.CharField(default=b'', max_length=200, verbose_name='\u573a\u666f')),
                ('startPoints_int', models.CharField(default=b'', max_length=200, verbose_name='\u96c6\u7ed3\u70b9')),
                ('zoneID', models.IntegerField(default=0, verbose_name='\u533a\u57dfID')),
                ('triggerInfos_int', models.CharField(default=b'', max_length=500, verbose_name='\u89e6\u53d1\u5668')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='PVPUpgradeScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rewards_int', models.CharField(default=b'', max_length=200, verbose_name='\u5956\u52b1')),
                ('mulLang', models.CharField(default=b'', max_length=200, verbose_name='\u90ae\u4ef6\u591a\u8bed\u8a00')),
                ('upgrade', models.CharField(default=b'', max_length=200, verbose_name='\u6bb5\u4f4d\u63cf\u8ff0\u591a\u8bed\u8a00')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
    ]
