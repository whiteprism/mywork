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
            name='Plot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gid', models.IntegerField(default=0, verbose_name='pk')),
                ('roleId', models.IntegerField(default=0, verbose_name='roleId')),
                ('serialIndex', models.IntegerField(default=0, verbose_name='serialIndex')),
                ('speakerType', models.IntegerField(default=0, verbose_name='speakerType')),
                ('dialogId', models.CharField(default=b'', max_length=200, verbose_name='dialogId')),
                ('animationType', models.IntegerField(default=0, verbose_name='animationType')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nameId', models.CharField(default=b'', max_length=50, verbose_name='\u540d\u79f0')),
                ('icon', models.CharField(default=b'', max_length=50, verbose_name='\u56fe\u6807')),
                ('level', models.IntegerField(default=0, verbose_name='level')),
                ('descriptionId', models.CharField(default=b'', max_length=200, verbose_name='pop text')),
                ('preGid', models.IntegerField(default=0, verbose_name='pre gid')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '\u65b0\u624b\u5f15\u5bfc',
                'verbose_name_plural': '\u65b0\u624b\u5f15\u5bfc',
            },
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='TutorialDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('guideGid', models.IntegerField(default=0, verbose_name='guideGid')),
                ('scenarioId', models.IntegerField(default=0, verbose_name='scenarioId')),
                ('step', models.IntegerField(default=0, verbose_name='step')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
    ]
