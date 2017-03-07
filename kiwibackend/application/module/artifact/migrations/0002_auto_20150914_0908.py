# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('artifact', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtifactAttribute',
            fields=[
                ('id', models.BigIntegerField(serialize=False, verbose_name='\u4e3b\u952e', primary_key=True)),
                ('attrType', models.CharField(max_length=200, verbose_name='attrType')),
                ('enhanceInitValue', models.FloatField(default=0, verbose_name='\u5f3a\u5316\u521d\u59cb\u503c')),
                ('enhanceAttrGrowth', models.FloatField(default=0, verbose_name='\u5f3a\u5316\u6210\u957f\u52a0\u503c')),
                ('refineInitValue', models.FloatField(default=0, verbose_name='\u7cbe\u70bc\u521d\u59cb\u503c')),
                ('refineAttrGrowth', models.FloatField(default=0, verbose_name='\u7cbe\u70bc\u6210\u957f\u52a0\u503c')),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='ArtifactEnhance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('xp', models.IntegerField(verbose_name='enhanceXp')),
                ('quality', models.IntegerField(verbose_name='\u5206\u7c7b')),
                ('level', models.IntegerField(verbose_name='level')),
                ('playerLevel', models.IntegerField(default=1, verbose_name='\u73a9\u5bb6\u7b49\u7ea7')),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='ArtifactRefine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quality', models.IntegerField(verbose_name='\u5206\u7c7b')),
                ('refineLevel', models.IntegerField(default=0, verbose_name='\u7cbe\u70bc\u7b49\u7ea7')),
                ('playerLevel', models.IntegerField(verbose_name='\u9700\u8981\u73a9\u5bb6\u7b49\u7ea7')),
                ('refineCost', models.IntegerField(verbose_name='\u7cbe\u70bc\u6d88\u8017')),
                ('artifactCount', models.IntegerField(default=0, verbose_name='\u9700\u8981\u6d88\u8017\u540c\u6837\u5723\u7269\u7684\u6570\u91cf')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.DeleteModel(
            name='ArtifactAttr',
        ),
        migrations.RemoveField(
            model_name='artifactlevel',
            name='artifact',
        ),
        migrations.AddField(
            model_name='artifact',
            name='attrList_int',
            field=models.CharField(default=0, max_length=200, verbose_name='\u5c5e\u6027\u914d\u7f6e'),
        ),
        migrations.AddField(
            model_name='artifact',
            name='skillId',
            field=models.IntegerField(default=0, verbose_name='\u6280\u80fdid'),
        ),
        migrations.DeleteModel(
            name='ArtifactLevel',
        ),
    ]
