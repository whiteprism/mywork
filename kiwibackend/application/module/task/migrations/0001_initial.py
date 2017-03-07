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
            name='DailyTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=200, verbose_name='name')),
                ('condition_id', models.IntegerField(default=0, verbose_name='condition id')),
                ('nameId', models.CharField(default=0, max_length=200, verbose_name='nameId')),
                ('rewards_int', models.CharField(default=b'', max_length=200, verbose_name='\u5956\u52b1ID,')),
                ('descriptionId', models.CharField(default=b'', max_length=200, verbose_name='\u63cf\u8ff0')),
                ('icon', models.CharField(default=b'', max_length=200, verbose_name='icon')),
                ('link', models.IntegerField(default=0, verbose_name='link')),
                ('level', models.IntegerField(default=0, verbose_name='\u89e3\u9501\u7b49\u7ea7')),
                ('orderId', models.IntegerField(default=0, verbose_name='\u6392\u5e8f')),
                ('category', models.IntegerField(default=0, verbose_name='\u7c7b\u522b')),
                ('nextTaskId', models.IntegerField(default=0, verbose_name='\u4e0b\u4e2a\u4efb\u52a1ID')),
                ('is_first', models.BooleanField(default=False, verbose_name='\u662f\u5426\u4e3a\u521d\u59cb\u4efb\u52a1')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=200, verbose_name='name')),
                ('nameId', models.CharField(default=0, max_length=200, verbose_name='nameId')),
                ('rewards_int', models.CharField(default=b'', max_length=200, verbose_name='\u5956\u52b1ID,')),
                ('descriptionId', models.CharField(default=b'', max_length=200, verbose_name='\u63cf\u8ff0')),
                ('icon', models.CharField(default=b'', max_length=200, verbose_name='icon')),
                ('link', models.IntegerField(default=0, verbose_name='link')),
                ('nextTaskId', models.IntegerField(default=0, verbose_name='\u4e0b\u4e2a\u4efb\u52a1ID')),
                ('level', models.IntegerField(default=0, verbose_name='\u5f00\u542f\u7b49\u7ea7')),
                ('orderId', models.IntegerField(default=0, verbose_name='\u6392\u5e8f')),
                ('category', models.IntegerField(default=0, verbose_name='\u7c7b\u522b')),
                ('is_first', models.BooleanField(default=False, verbose_name='\u662f\u5426\u4e3a\u521d\u59cb\u4efb\u52a1')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='TaskCondition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('c1_int', models.CharField(default=b'', max_length=100, verbose_name='condition1')),
                ('c2_int', models.CharField(default=b'', max_length=100, verbose_name='condition2')),
                ('count', models.IntegerField(default=0, verbose_name='\u76ee\u6807\u6570\u91cf')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='TaskReward',
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
        migrations.AddField(
            model_name='task',
            name='condition',
            field=models.ForeignKey(to='task.TaskCondition'),
        ),
    ]
