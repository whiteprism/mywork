# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('guild', '0002_guild_speedrewards_int'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuildFireBuff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buffName', models.CharField(default=b'', max_length=50, verbose_name='buff\u540d\u5b57')),
                ('fireIndex_int', models.CharField(default=b'', max_length=50, verbose_name='BUFF\u53ef\u4ee5\u5b58\u5728\u7684\u706b\u5806INDEX')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.RenameModel(
            old_name='GuildBoneFire',
            new_name='GuildFireBuffLevel',
        ),
    ]
