# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('offlinebonus', '0002_auto_20170103_1915'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfflineBonusDay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rewardIds_str', models.CharField(default=0, max_length=100, verbose_name='\u5956\u52b1ID')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='OfflineBonusLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rewardIds_str', models.CharField(default=0, max_length=100, verbose_name='\u5956\u52b1ID')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.DeleteModel(
            name='OfflineBonusBase',
        ),
    ]
