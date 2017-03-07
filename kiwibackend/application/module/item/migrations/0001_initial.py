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
            name='CouragePointStore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('couragepoint', models.IntegerField(default=0, verbose_name='\u52c7\u6c14\u70b9\u6570\u91cf')),
                ('item_id', models.IntegerField(default=0, verbose_name='\u7269\u54c1\u788e\u7247ID')),
                ('count', models.IntegerField(default=0, verbose_name='\u6570\u91cf')),
                ('orderId', models.IntegerField(default=0, verbose_name='\u6392\u5e8f')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=0, max_length=200, verbose_name='name')),
                ('boxId', models.IntegerField(default=0, verbose_name='\u5b9d\u7bb1id')),
                ('boxKeyId', models.IntegerField(default=0, verbose_name='\u5b9d\u7bb1\u94a5\u5319')),
                ('gashapon_id', models.IntegerField(default=0, verbose_name='\u62bd\u5956ID')),
                ('canUse', models.BooleanField(default=False, verbose_name='\u662f\u5426\u53ef\u4ee5\u4f7f\u7528')),
                ('description', models.CharField(default=0, max_length=200, verbose_name='desc')),
                ('descriptionId', models.CharField(default=b'', max_length=200, verbose_name='desc id')),
                ('exp', models.IntegerField(default=0, verbose_name='\u7ecf\u9a8c')),
                ('getRewards_int', models.CharField(default=b'', max_length=200, verbose_name='\u5956\u52b1')),
                ('gold', models.IntegerField(default=0, verbose_name='gold')),
                ('icon', models.CharField(default=b'', max_length=200, verbose_name='icon')),
                ('diamond', models.IntegerField(default=0, verbose_name='')),
                ('nameId', models.CharField(default=b'', max_length=200, verbose_name='nameId')),
                ('power', models.IntegerField(default=0, verbose_name='\u4f53\u529b')),
                ('waravoidTime', models.IntegerField(default=0, verbose_name='\u514d\u6218\u65f6\u95f4')),
                ('quality', models.IntegerField(default=0, verbose_name='quality')),
                ('orderId', models.IntegerField(default=0, verbose_name='orderId')),
                ('sp', models.IntegerField(default=0, verbose_name='\u8010\u529b')),
                ('category', models.IntegerField(default=0, verbose_name='type')),
                ('searchDifficuty_int', models.CharField(default=0, max_length=200, verbose_name='\u51fa\u5904\u6240\u5728\u5173\u5361\u7684\u96be\u5ea6')),
                ('searchInstances_int', models.CharField(default=0, max_length=200, verbose_name='\u51fa\u5904\u6240\u5728\u5173\u5361id')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='ItemCompose',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=0, max_length=200, verbose_name='name')),
                ('pos', models.IntegerField(default=0, verbose_name='\u90e8\u4f4dID')),
                ('searchDifficuty_int', models.CharField(default=b'', max_length=200, verbose_name='\u6389\u843d\u5173\u5361\u96be\u5ea6')),
                ('searchInstances_int', models.CharField(default=b'', max_length=200, verbose_name='\u6389\u843d\u5173\u5361')),
                ('icon', models.CharField(default=b'', max_length=200, verbose_name='icon')),
                ('nameId', models.CharField(default=b'', max_length=200, verbose_name='nameId')),
                ('itemId', models.IntegerField(default=0, verbose_name='\u5408\u6210\u540e\u7269\u54c1ID')),
                ('fragmentId', models.IntegerField(default=0, verbose_name='\u7269\u54c1ID')),
                ('descriptionId', models.CharField(default=b'', max_length=200, verbose_name='descriptionId')),
                ('num', models.IntegerField(default=0, verbose_name='\u9700\u8981\u788e\u7247\u6570\u91cf')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='ItemReward',
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
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=0, max_length=200, verbose_name='name')),
                ('nameId', models.CharField(default=0, max_length=200, verbose_name='goodsName')),
                ('baseDiamond', models.IntegerField(default=0, verbose_name='\u57fa\u7840\u4ef7\u683c')),
                ('incrDiamond', models.IntegerField(default=0, verbose_name='\u8d2d\u4e70\u4ef7\u683c\u4e0a\u5347')),
                ('dailyCount', models.IntegerField(default=0, verbose_name='\u6bcf\u65e5\u9650\u8d2d\u4e0a\u9650')),
                ('item_id', models.IntegerField(default=0, verbose_name='item')),
                ('display', models.BooleanField(default=True, verbose_name='\u662f\u5426\u663e\u793a')),
                ('orderId', models.IntegerField(default=0, verbose_name='\u6392\u5e8f')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
    ]
