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
            name='Vip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('diamond', models.IntegerField(default=0, verbose_name='\u6bcf\u4e2a\u7b49\u7ea7\u5145\u503c\u989d\u5ea6')),
                ('sweepCount', models.IntegerField(default=0, verbose_name='\u626b\u8361\u5238\u6570\u91cf')),
                ('refreshMysteryShopCount', models.IntegerField(default=0, verbose_name='\u795e\u79d8\u5546\u5e97\u514d\u8d39\u5237\u65b0')),
                ('buyPowerCount', models.IntegerField(default=0, verbose_name='\u4f53\u529b\u8d2d\u4e70\u6b21\u6570')),
                ('buyGoldBoxCount', models.IntegerField(default=0, verbose_name='\u91d1\u5b9d\u7bb1\u8d2d\u4e70\u6b21\u6570')),
                ('buyStaminaCount', models.IntegerField(default=0, verbose_name='\u8010\u529b\u8d2d\u4e70\u6b21\u6570')),
                ('goldHandCount', models.IntegerField(default=0, verbose_name='\u70b9\u91d1\u624b\u8d2d\u4e70\u6b21\u6570')),
                ('resetElitInstanceCount', models.IntegerField(default=0, verbose_name='\u91cd\u7f6e\u7cbe\u82f1\u5173\u5361\u6b21\u6570')),
                ('titanCount', models.IntegerField(default=0, verbose_name='\u6cf0\u5766\u6b21\u6570')),
                ('timeGateCount', models.IntegerField(default=0, verbose_name='\u65f6\u7a7a\u4e4b\u95e8\u6b21\u6570')),
                ('giftBagNameId', models.CharField(default=b'', max_length=200, verbose_name='\u793c\u5305\u540dID')),
                ('giftBagDiamond', models.IntegerField(default=0, verbose_name='\u793c\u5305\u4ef7\u683c')),
                ('giftRewards_int', models.CharField(default=b'', max_length=200, verbose_name='\u5956\u52b1')),
                ('descriptionId', models.CharField(default=b'', max_length=200, verbose_name='\u63cf\u8ff0Id')),
                ('growthFund', models.IntegerField(default=0, verbose_name='\u80fd\u5426\u8d2d\u4e70\u6210\u957f\u57fa\u91d1')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='VipReward',
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
