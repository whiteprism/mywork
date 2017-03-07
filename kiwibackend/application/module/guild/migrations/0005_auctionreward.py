# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('guild', '0004_guildfirelevel'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuctionReward',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('basePrice', models.IntegerField(default=0, verbose_name='\u8d77\u6b65\u4ef7\u683c')),
                ('stepPrice', models.IntegerField(default=0, verbose_name='\u4ef7\u683c\u6b65\u957f')),
                ('maxPrice', models.IntegerField(default=0, verbose_name='\u4ef7\u683c\u6b65\u957f')),
                ('rewardId', models.CharField(max_length=50, verbose_name=b'rewardId string')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
    ]
