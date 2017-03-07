# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0006_auto_20160808_1646'),
    ]

    operations = [
        migrations.CreateModel(
            name='SevenDaysHalfPrice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('itemName', models.CharField(default=b'', max_length=200, verbose_name='\u9053\u5177\u540d\u5b57,')),
                ('itemNameMul', models.CharField(default=b'', max_length=200, verbose_name='\u9053\u5177\u540d\u5b57\u591a\u8bed\u8a00,')),
                ('itemCost', models.IntegerField(default=0, verbose_name='\u7269\u54c1\u82b1\u8d39')),
                ('itemType', models.IntegerField(default=0, verbose_name='\u7269\u54c1\u5206\u7c7b')),
                ('limitDay', models.IntegerField(default=0, verbose_name='\u7b2c\u51e0\u5929\u5f00\u542f')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
    ]
