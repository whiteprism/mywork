# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('guild', '0006_auto_20161026_0954'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuildSiegeBattleReward',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rewardIds1_str', models.CharField(max_length=100, verbose_name=b'rewardId string level 1')),
                ('rewardIds2_str', models.CharField(max_length=100, verbose_name=b'rewardId string level 2')),
                ('rewardIds3_str', models.CharField(max_length=100, verbose_name=b'rewardId string level 3')),
                ('rewardIds4_str', models.CharField(max_length=100, verbose_name=b'rewardId string level 4')),
                ('rewardIds5_str', models.CharField(max_length=100, verbose_name=b'rewardId string level 5')),
                ('rewardIds6_str', models.CharField(max_length=100, verbose_name=b'rewardId string level 6')),
                ('rewardIds7_str', models.CharField(max_length=100, verbose_name=b'rewardId string level 7')),
                ('rewardIds8_str', models.CharField(max_length=100, verbose_name=b'rewardId string level 8')),
                ('rewardIds9_str', models.CharField(max_length=100, verbose_name=b'rewardId string level 9')),
                ('rewardIds10_str', models.CharField(max_length=100, verbose_name=b'rewardId string level 10')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
    ]
