# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nameId', models.CharField(default=b'', max_length=100, verbose_name='\u540d\u5b57')),
                ('iconId', models.CharField(default=b'', max_length=100, verbose_name='\u56fe\u6807')),
                ('category', models.IntegerField(default=0, verbose_name='\u6d3b\u52a8\u7c7b\u578b')),
                ('beginTime', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6d3b\u52a8\u5f00\u59cb\u65f6\u95f4')),
                ('endTime', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6d3b\u52a8\u7ed3\u675f\u65f6\u95f4')),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='ActivityReward',
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
        migrations.CreateModel(
            name='ActivityRule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activityId', models.IntegerField(default=0, verbose_name='\u6d3b\u52a8\u7684id(Activity id)')),
                ('giftBagId', models.IntegerField(default=0, verbose_name='\u793c\u5305\u5956\u52b1gid')),
                ('value1', models.IntegerField(default=0, verbose_name='valueInt')),
                ('value2', models.IntegerField(default=0, verbose_name='\u5907\u7528\u5b57\u6bb52')),
                ('value3', models.IntegerField(default=0, verbose_name='\u5907\u7528\u5b57\u6bb53')),
                ('value4', models.IntegerField(default=0, verbose_name='\u5907\u7528\u5b57\u6bb54')),
                ('value5', models.IntegerField(default=0, verbose_name='\u5907\u7528\u5b57\u6bb55')),
                ('value6', models.IntegerField(default=0, verbose_name='\u5907\u7528\u5b57\u6bb56')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='GiftPackage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.IntegerField(default=0, verbose_name='\u6d3b\u52a8\u7c7b\u578b')),
                ('name', models.CharField(max_length=100, verbose_name='\u540d\u5b57')),
                ('entryName_key', models.CharField(max_length=100, verbose_name='entry\u540d\u5b57key')),
                ('entryName_val', models.CharField(max_length=100, verbose_name='entry\u540d\u5b57value')),
                ('level', models.IntegerField(default=0, verbose_name='\u7b49\u7ea7')),
                ('rewards_int', models.CharField(default=b'', max_length=200, verbose_name='\u5956\u52b1\u7684id list')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
    ]
