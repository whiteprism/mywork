# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0005_auto_20160718_0933'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyTaskActivity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activityValue', models.IntegerField(default=0, verbose_name='\u4efb\u52a1\u6761\u4ef6ID')),
                ('rewards_int', models.CharField(default=b'', max_length=200, verbose_name='\u5956\u52b1ID,')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.AddField(
            model_name='dailytask',
            name='activityGet',
            field=models.IntegerField(default=0, verbose_name='\u53ef\u4ee5\u83b7\u53d6\u7684\u6d3b\u8dc3\u5ea6'),
        ),
    ]
