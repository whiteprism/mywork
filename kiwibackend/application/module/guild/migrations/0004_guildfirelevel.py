# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('guild', '0003_auto_20161024_1032'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuildFireLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('xp', models.IntegerField(default=0, verbose_name='\u706b\u5806\u7b49\u7ea7\u6240\u9700\u7ecf\u9a8c')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
    ]
