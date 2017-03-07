# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_auto_20160128_1735'),
    ]

    operations = [
        migrations.CreateModel(
            name='SevenDaysTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=200, verbose_name='name')),
                ('condition_id', models.IntegerField(default=0, verbose_name='\u4efb\u52a1\u6761\u4ef6ID')),
                ('nameId', models.CharField(default=0, max_length=200, verbose_name='nameId')),
                ('rewards_int', models.CharField(default=b'', max_length=200, verbose_name='\u5956\u52b1ID,')),
                ('descriptionId', models.CharField(default=b'', max_length=200, verbose_name='\u63cf\u8ff0')),
                ('icon', models.CharField(default=b'', max_length=200, verbose_name='icon')),
                ('link', models.IntegerField(default=0, verbose_name='link')),
                ('nextTaskId', models.IntegerField(default=0, verbose_name='\u4e0b\u4e2a\u4efb\u52a1ID')),
                ('level', models.IntegerField(default=0, verbose_name='\u5f00\u542f\u7b49\u7ea7')),
                ('orderId', models.IntegerField(default=0, verbose_name='\u6392\u5e8f')),
                ('category', models.IntegerField(default=0, verbose_name='\u7c7b\u522b')),
                ('is_first', models.BooleanField(default=False, verbose_name='\u662f\u5426\u4e3a\u521d\u59cb\u4efb\u52a1')),
                ('buildingId', models.IntegerField(default=0, verbose_name='\u5165\u53e3\u5efa\u7b51')),
                ('limitDay', models.IntegerField(default=0, verbose_name='\u65f6\u95f4\u9650\u5236')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
    ]
