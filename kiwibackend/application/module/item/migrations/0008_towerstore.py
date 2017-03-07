# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0007_auto_20160811_1453'),
    ]

    operations = [
        migrations.CreateModel(
            name='TowerStore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=0, max_length=200, verbose_name='name')),
                ('nameId', models.CharField(default=0, max_length=200, verbose_name='goodsName')),
                ('basePrice', models.IntegerField(default=0, verbose_name='\u57fa\u7840\u4ef7\u683c')),
                ('incrPrice', models.IntegerField(default=0, verbose_name='\u8d2d\u4e70\u4ef7\u683c\u4e0a\u5347')),
                ('dailyCount', models.IntegerField(default=0, verbose_name='\u6bcf\u65e5\u9650\u8d2d\u4e0a\u9650')),
                ('item_id', models.IntegerField(default=0, verbose_name='item')),
                ('display', models.BooleanField(default=True, verbose_name='\u662f\u5426\u663e\u793a')),
                ('orderId', models.IntegerField(default=0, verbose_name='\u6392\u5e8f')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
    ]
