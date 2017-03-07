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
            name='ArenaShop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='\u540d\u5b57')),
                ('itemId', models.IntegerField(default=0, verbose_name='gid')),
                ('count', models.IntegerField(default=0, verbose_name='count')),
                ('score', models.IntegerField(default=0, verbose_name='score')),
                ('category', models.IntegerField(default=0, verbose_name='\u5206\u7c7b')),
                ('probability', models.IntegerField(default=0, verbose_name='\u6982\u7387')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
    ]
