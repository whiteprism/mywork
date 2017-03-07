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
            name='Guild',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.IntegerField(default=0, verbose_name='\u516c\u4f1a\u7b49\u7ea7')),
                ('unlockFunction_int', models.CharField(default=b'', max_length=200, verbose_name='\u5f00\u653e\u529f\u80fd')),
                ('viceChairmanCount', models.IntegerField(default=0, verbose_name='\u526f\u4f1a\u957f\u4e2a\u6570')),
                ('memberCount', models.IntegerField(default=0, verbose_name='\u516c\u4f1a\u6210\u5458\u4e2a\u6570')),
                ('xp', models.IntegerField(default=0, verbose_name='\u9700\u8981\u7ecf\u9a8c')),
                ('speedCount', models.IntegerField(default=0, verbose_name='\u52a0\u901f\u6b21\u6570')),
                ('beSpeededCount', models.IntegerField(default=0, verbose_name='\u88ab\u52a0\u901f\u6b21\u6570')),
                ('levelUpCost', models.IntegerField(default=0, verbose_name='\u5347\u7ea7\u9700\u8981\u82b1\u8d39\u94bb\u77f3')),
                ('chairmanBouns', models.IntegerField(default=0, verbose_name='\u4f1a\u957f\u8fd4\u5229')),
                ('vichairmanBonus', models.IntegerField(default=0, verbose_name='\u526f\u4f1a\u957f\u8fd4\u5229')),
                ('memberBouns', models.IntegerField(default=0, verbose_name='\u6210\u5458\u8fd4\u5229')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='GuildBoneFire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fireLevel', models.IntegerField(default=0, verbose_name='\u706b\u5806\u7b49\u7ea7')),
                ('buffType', models.IntegerField(default=0, verbose_name='buff\u7c7b\u578b')),
                ('buffValue', models.FloatField(default=0, verbose_name='buff\u503c')),
                ('buffLevel', models.IntegerField(default=0, verbose_name='buff\u7b49\u7ea7')),
                ('woodCost', models.IntegerField(default=0, verbose_name='\u6d88\u8017\u6728\u5934')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='GuildShop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='\u540d\u5b57')),
                ('itemId', models.IntegerField(default=0, verbose_name='gid')),
                ('count', models.IntegerField(default=0, verbose_name='count')),
                ('cost', models.IntegerField(default=0, verbose_name='\u6d88\u8017')),
                ('category', models.IntegerField(default=0, verbose_name='\u5206\u7c7b')),
                ('show_id', models.IntegerField(default=0, verbose_name='\u6392\u5e8f')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
    ]
