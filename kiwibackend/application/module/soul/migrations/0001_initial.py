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
            name='Soul',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('warrior_id', models.IntegerField(verbose_name='\u82f1\u96c4id')),
                ('name', models.CharField(max_length=200, verbose_name='\u788e\u7247\u540d\u79f0')),
                ('couragePoint', models.IntegerField(verbose_name='\u4e00\u4e2a\u7075\u9b42\u788e\u7247\u5bf9\u5e94\u7684N\u4e2a\u5fbd\u7ae0')),
                ('descriptionId', models.CharField(default=b'', max_length=200, verbose_name='')),
                ('searchDifficuty_int', models.CharField(default=b'', max_length=200, verbose_name='\u8be5\u9b42\u9b44\u5728\u54ea\u91cc\u6389\u843d\u90a3\u91cc\u7684\u96be\u5ea6')),
                ('searchInstances_int', models.CharField(default=b'', max_length=200, verbose_name='\u8be5\u9b42\u9b44\u5728\u54ea\u4e9b\u5173\u5361\u4f1a\u6389\u843d')),
                ('gold', models.IntegerField(verbose_name='\u4e00\u4e2a\u7075\u9b42\u788e\u7247\u5bf9\u5e94\u5206\u89e3\u51fa\u6765\u7684\u94b1\u6570')),
                ('icon', models.CharField(max_length=200, verbose_name='icon')),
                ('nameId', models.CharField(max_length=200, verbose_name='nameId')),
                ('quality', models.IntegerField(verbose_name='\u6b21\u7ec4\u914d\u7f6e\u4e2d\uff0c\u8be5\u7075\u9b42\u788e\u7247\u7684\u4e2a\u6570')),
                ('recruitCost', models.IntegerField(verbose_name='\u5408\u6210\u76ee\u6807\u82f1\u96c4\u7684\u4ef7\u683c')),
                ('breakCost', models.IntegerField(verbose_name='\u83b7\u5f97\u82f1\u96c4\u5206\u89e3\u83b7\u5f97\u7075\u9b42\u788e\u7247\u4e2a\u6570')),
                ('recruitHeroId', models.IntegerField(verbose_name='\u8c01\u7684\u7075\u9b42\u788e\u7247')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
    ]
