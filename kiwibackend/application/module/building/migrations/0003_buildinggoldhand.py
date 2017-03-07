# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0002_buildingradar'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingGoldHand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('critTwo', models.IntegerField(default=0, verbose_name='\u4e24\u500d\u66b4\u51fb\u6982\u7387')),
                ('critThree', models.IntegerField(default=0, verbose_name='\u4e09\u500d\u66b4\u51fb\u6982\u7387')),
                ('critFive', models.IntegerField(default=0, verbose_name='\u4e94\u500d\u66b4\u51fb\u6982\u7387')),
                ('critTen', models.IntegerField(default=0, verbose_name='\u5341\u500d\u66b4\u51fb\u6982\u7387')),
                ('critProperbility', models.IntegerField(default=0, verbose_name='\u662f\u5426\u66b4\u51fb\u6982\u7387')),
                ('expectGold', models.IntegerField(default=0, verbose_name='\u9884\u8ba1\u91d1\u989d')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
    ]
