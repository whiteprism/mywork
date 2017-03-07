# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0006_raidlevelconf_suggestheroids_int'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElementTowerBuff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attrs_int', models.CharField(default=b'', max_length=300, verbose_name='\u5c5e\u6027s')),
                ('extras_float', models.CharField(default=b'', max_length=300, verbose_name='\u5c5e\u6027\u52a0\u6210')),
                ('iconId', models.CharField(default=b'', max_length=50, verbose_name='ICON')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='ElementTowerInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=50, verbose_name='\u540d\u5b57')),
                ('iconId', models.CharField(default=b'', max_length=50, verbose_name='ICON')),
                ('bgImageId', models.CharField(default=b'', max_length=50, verbose_name='background image ID')),
                ('extroImageId', models.CharField(default=b'', max_length=50, verbose_name='extro image ID')),
                ('difficulty', models.IntegerField(default=0, verbose_name='\u96be\u5ea6')),
                ('minUserLevel', models.IntegerField(default=0, verbose_name='\u73a9\u5bb6\u6700\u5c0f\u7b49\u7ea7')),
                ('scene', models.CharField(default=b'', max_length=50, verbose_name='\u573a\u666f')),
                ('rewardIds_str', models.CharField(default=b'', max_length=300, verbose_name='\u5956\u52b1ID')),
                ('enemyIds_int', models.CharField(default=b'', max_length=300, verbose_name='\u654c\u519b\u9635\u5bb9ID')),
                ('zoneIDs_int', models.CharField(default=b'', max_length=300, verbose_name='zone ID')),
                ('suggestHeroIds_int', models.CharField(default=b'', max_length=300, verbose_name='\u63a8\u8350\u9635\u5bb9')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='ElementTowerLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('monsterId', models.IntegerField(default=0, verbose_name='\u602a\u7269')),
                ('towerId', models.IntegerField(default=0, verbose_name='\u5854ID')),
                ('level', models.IntegerField(default=0, verbose_name='\u5c42\u7ea7')),
                ('rewardIds_str', models.CharField(default=b'', max_length=300, verbose_name='\u5956\u52b1')),
                ('difficulty', models.IntegerField(default=0, verbose_name='\u96be\u5ea6')),
                ('diamondRewardIds_str', models.CharField(default=b'', max_length=300, verbose_name='\u94bb\u77f3\u5f00\u5b9d\u7bb1')),
                ('diamondCosts_int', models.CharField(default=b'', max_length=300, verbose_name='\u94bb\u77f3\u5f00\u5b9d\u7bb1\u6d88\u8017')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.DeleteModel(
            name='RaidEnemyToReward',
        ),
        migrations.DeleteModel(
            name='RaidInstanceReward',
        ),
        migrations.DeleteModel(
            name='RaidLevelBuff',
        ),
        migrations.DeleteModel(
            name='RaidLevelDifficulty',
        ),
    ]
