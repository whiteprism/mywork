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
            name='Artifact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=0, max_length=200, verbose_name='name')),
                ('upgradeXp', models.IntegerField(default=0, verbose_name='\u5f3a\u5316\u65f6\u63d0\u4f9b\u57fa\u7840\u7ecf\u9a8c')),
                ('icon', models.CharField(default=b'', max_length=200, verbose_name='icon')),
                ('descriptionId', models.CharField(default=b'', max_length=200, verbose_name='descriptionId')),
                ('nameId', models.CharField(default=b'', max_length=200, verbose_name='nameId')),
                ('quality', models.IntegerField(default=0, verbose_name='\u54c1\u8d28')),
                ('orderId', models.IntegerField(default=0, verbose_name='\u663e\u793a\u987a\u5e8f')),
                ('composeFragmentIds_int', models.CharField(default=b'', max_length=200, verbose_name='\u5723\u7269\u788e\u7247ID')),
                ('category', models.IntegerField(default=0, verbose_name='category')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='ArtifactAttr',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attrType', models.CharField(default=0, max_length=200, verbose_name='attrType')),
                ('extra', models.FloatField(default=0, verbose_name='extra')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='ArtifactFragment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=0, max_length=200, verbose_name='name')),
                ('pos', models.IntegerField(default=0, verbose_name='\u788e\u7247\u90e8\u4f4dID')),
                ('searchDifficuty_int', models.CharField(default=b'', max_length=200, verbose_name='\u6389\u843d\u5173\u5361\u96be\u5ea6')),
                ('searchInstances_int', models.CharField(default=b'', max_length=200, verbose_name='\u6389\u843d\u5173\u5361')),
                ('icon', models.CharField(default=b'', max_length=200, verbose_name='icon')),
                ('nameId', models.CharField(default=b'', max_length=200, verbose_name='nameId')),
                ('artifactId', models.IntegerField(default=0, verbose_name='\u5408\u6210\u540e\u5723\u7269ID')),
                ('descriptionId', models.CharField(default=b'', max_length=200, verbose_name='descriptionId')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='ArtifactLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.IntegerField(default=0, verbose_name='\u7b49\u7ea7')),
                ('attrs_int', models.CharField(default=0, max_length=200, verbose_name='attr list')),
                ('needXp', models.IntegerField(default=0, verbose_name='\u5347\u5230\u5bf9\u5e94\u7b49\u7ea7\u6240\u9700\u7ecf\u9a8c')),
                ('skillId', models.IntegerField(default=0, verbose_name='\u6280\u80fdID')),
                ('skillLevel', models.IntegerField(default=0, verbose_name='\u6280\u80fd\u7b49\u7ea7')),
                ('artifactElement', models.IntegerField(default=0, verbose_name='\u6d88\u8017\u5143\u7d20\u4e4b\u6838')),
                ('artifact', models.ForeignKey(to='artifact.Artifact')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
    ]
