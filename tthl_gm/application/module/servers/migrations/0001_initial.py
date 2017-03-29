# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ServerInfo',
            fields=[
                ('id', models.IntegerField(serialize=False, verbose_name='\u670d\u52a1\u5668ID', primary_key=True)),
                ('code', models.CharField(default=b'', max_length=30, verbose_name='\u670d\u52a1\u5668\u4ee3\u53f7')),
                ('zone_id', models.IntegerField(default=1, verbose_name='\u533a\u57dfID')),
                ('zone_name', models.CharField(max_length=30, verbose_name='\u533a\u57df\u540d\u79f0')),
                ('name', models.CharField(unique=True, max_length=20, verbose_name='\u670d\u52a1\u5668\u540d\u79f0')),
                ('url', models.CharField(max_length=200, null=True, verbose_name='\u8fde\u63a5\u5730\u5740', blank=True)),
                ('status_id', models.IntegerField(default=1, verbose_name='\u670d\u52a1\u5668\u72b6\u6001ID')),
                ('status_text', models.CharField(max_length=20, verbose_name='\u670d\u52a1\u5668\u72b6\u6001\u63cf\u8ff0')),
                ('open_at', models.CharField(max_length=200, verbose_name='\u5f00\u670d\u65f6\u95f4')),
                ('gm_url', models.CharField(max_length=200, null=True, verbose_name='\u8fde\u63a5\u5730\u5740', blank=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
