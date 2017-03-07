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
            name='Package',
            fields=[
                ('id', models.CharField(max_length=30, serialize=False, verbose_name=b'\xe7\xa4\xbc\xe5\x8c\x85ID', primary_key=True)),
                ('name', models.CharField(default=b'', max_length=20, verbose_name='\u793c\u5305\u6807\u793a')),
                ('batch', models.CharField(default=b'', max_length=20, verbose_name='\u6279\u6b21')),
                ('rewards_int', models.CharField(default=0, max_length=100, verbose_name='\u5956\u52b1ID')),
                ('channels_str', models.CharField(default=0, max_length=200, verbose_name='\u6e20\u9053ID')),
                ('serverids_int', models.CharField(default=0, max_length=100, verbose_name='\u670d\u52a1\u5668ID')),
                ('expire_date', models.CharField(default=0, max_length=50, verbose_name='\u8fc7\u671f\u65f6\u95f4')),
                ('gift_title', models.CharField(default=0, max_length=100, verbose_name='\u793c\u7269\u6807\u9898')),
                ('gift_body', models.CharField(default=0, max_length=200, verbose_name='\u793c\u7269\u5185\u5bb9')),
                ('code_count', models.IntegerField(default=0, verbose_name='\u4f7f\u7528\u7684\u7528\u6237ID')),
                ('tag', models.CharField(default=0, max_length=50, verbose_name='\u751f\u6210\u8def\u5f84')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='PackageCode',
            fields=[
                ('id', models.CharField(max_length=30, serialize=False, verbose_name=b'\xe7\xa4\xbc\xe5\x8c\x85\xe7\xbc\x96\xe7\xa0\x81', primary_key=True)),
                ('package_id', models.CharField(max_length=30, verbose_name=b'\xe7\xa4\xbc\xe5\x8c\x85\xe7\xbc\x96\xe7\xa0\x81')),
                ('is_use', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe4\xbd\xbf\xe7\x94\xa8')),
                ('use_serverid', models.CharField(default=b'', max_length=20, verbose_name='\u4f7f\u7528\u670d\u52a1\u5668ID')),
                ('use_playerid', models.IntegerField(default=0, verbose_name='\u4f7f\u7528\u7684\u7528\u6237ID')),
                ('created_at', models.DateTimeField(verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('used_at', models.DateTimeField(verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
            ],
        ),
        migrations.CreateModel(
            name='PackageReward',
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
    ]
