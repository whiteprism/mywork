# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('equip', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipSuit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pos1Id', models.IntegerField(verbose_name='\u6b66\u5668')),
                ('pos2Id', models.IntegerField(verbose_name='\u5934\u76d4')),
                ('pos3Id', models.IntegerField(verbose_name='\u8863\u670d')),
                ('pos4Id', models.IntegerField(verbose_name='\u88e4\u5b50')),
                ('attr2List_int', models.CharField(max_length=200, verbose_name='2\u4ef6\u88c5\u5907\u5c5e\u6027\u52a0\u6210')),
                ('attr3List_int', models.CharField(max_length=200, verbose_name='3\u4ef6\u88c5\u5907\u5c5e\u6027\u52a0\u6210')),
                ('attr4List_int', models.CharField(max_length=200, verbose_name='4\u4ef6\u88c5\u5907\u5c5e\u6027\u52a0\u6210')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.CreateModel(
            name='EquipSuitAttr',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attrType', models.CharField(default=0, max_length=200, verbose_name='attrType')),
                ('extra', models.FloatField(default=0, verbose_name='extra')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
        migrations.RemoveField(
            model_name='cardequipinfo',
            name='pos5_int',
        ),
        migrations.RemoveField(
            model_name='cardequipinfo',
            name='pos6_int',
        ),
        migrations.RemoveField(
            model_name='cardequipinfo',
            name='pos7_int',
        ),
        migrations.AddField(
            model_name='equip',
            name='equipSuitId',
            field=models.IntegerField(default=0, verbose_name='\u5957\u88c5ID'),
        ),
    ]
