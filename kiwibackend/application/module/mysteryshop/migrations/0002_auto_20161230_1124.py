# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('mysteryshop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MysteryShopGrid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('categories_int', models.CharField(default=b'', max_length=50, verbose_name='\u5956\u52b1Id')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.RemoveField(
            model_name='mysteryshop',
            name='category',
        ),
        migrations.RemoveField(
            model_name='mysteryshop',
            name='itemId',
        ),
        migrations.AddField(
            model_name='mysteryshop',
            name='rewardId',
            field=models.CharField(default=b'', max_length=50, verbose_name='\u5956\u52b1Id'),
        ),
        migrations.AddField(
            model_name='mysteryshop',
            name='vipLevelLimit',
            field=models.IntegerField(default=0, verbose_name='VIP\u7b49\u7ea7\u9650\u5236'),
        ),
    ]
