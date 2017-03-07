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
            name='LoginBonus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rewards_int', models.CharField(default=0, max_length=100, verbose_name='\u5956\u52b1ID')),
                ('gift_title', models.CharField(default=0, max_length=100, verbose_name='\u793c\u7269\u6807\u9898')),
                ('gift_body', models.CharField(default=0, max_length=200, verbose_name='\u793c\u7269\u5185\u5bb9')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='LoginBonusReward',
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
