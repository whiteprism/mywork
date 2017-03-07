# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0003_auto_20160107_1848'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemSuit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('boxNameId', models.CharField(default=b'', max_length=200, verbose_name='\u5b9d\u7bb1id')),
                ('introduction', models.CharField(default=b'', max_length=500, verbose_name='\u5b9d\u7bb1\u8bf4\u660e\u5185\u5bb9')),
                ('iconId', models.IntegerField(default=0, verbose_name='\u5b9d\u7bb1\u56fe\u6807')),
                ('itemIds_int', models.CharField(default=b'', max_length=200, verbose_name='\u5305\u542b\u7269\u54c1id')),
                ('itemCounts_int', models.CharField(default=b'', max_length=200, verbose_name='\u5305\u542b\u7269\u54c1\u6570\u91cf')),
                ('isChooseAll', models.IntegerField(default=0, verbose_name='\u662f\u5426\u53ef\u9009\u5168\u90e8')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.AddField(
            model_name='item',
            name='isChapter',
            field=models.IntegerField(default=0, verbose_name='\u7ae0\u8282\u5224\u65ad'),
        ),
        migrations.AlterField(
            model_name='item',
            name='searchDifficuty_int',
            field=models.CharField(default=b'', max_length=200, verbose_name='\u51fa\u5904\u6240\u5728\u5173\u5361\u7684\u96be\u5ea6'),
        ),
        migrations.AlterField(
            model_name='item',
            name='searchInstances_int',
            field=models.CharField(default=b'', max_length=200, verbose_name='\u51fa\u5904\u6240\u5728\u5173\u5361id'),
        ),
    ]
