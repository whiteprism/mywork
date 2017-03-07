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
            name='Yuanbo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=50, verbose_name='\u540d\u79f0')),
                ('iconId', models.CharField(default=b'', max_length=50, verbose_name='\u540d\u79f0')),
                ('price', models.IntegerField(default=0, verbose_name='\u5e73\u53f0\u4ef7\u683c')),
                ('amount', models.IntegerField(default=0, verbose_name='\u8d2d\u4e70\u5143\u5b9d\u6570\u91cf')),
                ('first_amount', models.IntegerField(default=0, verbose_name='\u5956\u52b1\u5143\u5b9d\u6570\u91cf')),
                ('reward_amount', models.IntegerField(default=0, verbose_name='\u5956\u52b1\u5143\u5b9d\u6570\u91cf')),
                ('is_ios', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '\u5143\u5b9d\u6570\u636e',
                'verbose_name_plural': '\u5143\u5b9d\u6570\u636e',
            },
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
    ]
