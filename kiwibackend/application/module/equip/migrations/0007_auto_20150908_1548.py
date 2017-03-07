# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('equip', '0006_auto_20150908_1356'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipRefine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quality', models.IntegerField(verbose_name='\u5206\u7c7b')),
                ('refineLevel', models.IntegerField(default=0, verbose_name='\u7cbe\u70bc\u7b49\u7ea7')),
                ('equipLevel', models.IntegerField(default=1, verbose_name='\u88c5\u5907\u7b49\u7ea7')),
                ('refineCost', models.IntegerField(verbose_name='\u7cbe\u70bc\u6d88\u8017')),
                ('goldCost', models.IntegerField(verbose_name='\u91d1\u5e01\u6d88\u8017')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.RemoveField(
            model_name='equipattribute',
            name='attrGrowth',
        ),
        migrations.AddField(
            model_name='equipattribute',
            name='enhanceAttrGrowth',
            field=models.FloatField(default=0, verbose_name='\u5f3a\u5316\u6210\u957f\u52a0\u503c'),
        ),
        migrations.AddField(
            model_name='equipattribute',
            name='refineAttrGrowth',
            field=models.FloatField(default=0, verbose_name='\u7cbe\u70bc\u6210\u957f\u52a0\u503c'),
        ),
        migrations.AlterField(
            model_name='equipattribute',
            name='initValue',
            field=models.FloatField(default=0, verbose_name='\u521d\u59cb\u503c'),
        ),
    ]
