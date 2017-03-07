# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('pvp', '0003_auto_20161222_0919'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiegeAttactSoldierInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(default=0, verbose_name='\u58eb\u5175\u7c7b\u578b')),
                ('name', models.CharField(default=0, max_length=200, verbose_name='name')),
                ('energyConsume', models.IntegerField(default=0, verbose_name='\u80fd\u91cf\u6d88\u8017')),
                ('maxCount', models.IntegerField(default=0, verbose_name='\u6700\u5927\u6295\u653e\u6570\u91cf')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
    ]
