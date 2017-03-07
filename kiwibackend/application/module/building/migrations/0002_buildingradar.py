# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingRadar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('building', models.IntegerField(default=0, verbose_name='\u5efa\u7b51id')),
                ('level', models.IntegerField(default=0, verbose_name='\u7b49\u7ea7')),
                ('count', models.IntegerField(default=0, verbose_name='\u589e\u52a0\u641c\u7d22\u6570\u91cf')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
    ]
