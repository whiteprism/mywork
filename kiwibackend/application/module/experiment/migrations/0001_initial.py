# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.CharField(max_length=100, serialize=False, verbose_name=b'\xe5\xae\x9e\xe9\xaa\x8c\xe5\x90\x8d\xe7\xa7\xb0', primary_key=True)),
                ('whitelist', models.TextField(help_text=b'\xe6\xad\xa4\xe7\x99\xbd\xe5\x90\x8d\xe5\x8d\x95\xe4\xb8\xba\xe9\x99\x84\xe5\x8a\xa0\xe7\x99\xbd\xe5\x90\x8d\xe5\x8d\x95', verbose_name=b'\xe7\x99\xbd\xe5\x90\x8d\xe5\x8d\x95', blank=True)),
                ('blacklist', models.TextField(help_text=b'\xe6\xad\xa4\xe9\xbb\x91\xe5\x90\x8d\xe5\x8d\x95\xe4\xb8\xba\xe9\x99\x84\xe5\x8a\xa0\xe9\xbb\x91\xe5\x90\x8d\xe5\x8d\x95', verbose_name=b'\xe9\xbb\x91\xe5\x90\x8d\xe5\x8d\x95', blank=True)),
                ('started_at1', models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0), verbose_name='\u5f00\u59cb\u65f6\u95f41')),
                ('ended_at1', models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0), verbose_name='\u7ed3\u675f\u65f6\u95f41')),
                ('started_at2', models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0), verbose_name='\u5f00\u59cb\u65f6\u95f42')),
                ('ended_at2', models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0), verbose_name='\u7ed3\u675f\u65f6\u95f42')),
                ('started_at3', models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0), verbose_name='\u5f00\u59cb\u65f6\u95f43')),
                ('ended_at3', models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0), verbose_name='\u7ed3\u675f\u65f6\u95f43')),
                ('weekdays_str', models.TextField(help_text=b'\xe4\xbb\xa5\xe5\x8d\x8a\xe8\xa7\x92,\xe5\x88\x86\xe5\x89\xb2', verbose_name=b'\xe6\x98\x9f\xe6\x9c\x9f', blank=True)),
                ('week_started_at', models.TimeField(default=datetime.time(0, 0), verbose_name='\u6bcf\u5468\u51e0\u5f00\u59cb\u65f6\u95f4')),
                ('week_ended_at', models.TimeField(default=datetime.time(0, 0), verbose_name='\u6bcf\u5468\u51e0\u7ed3\u675f\u65f6\u95f4')),
                ('monthdays_str', models.TextField(help_text=b'\xe4\xbb\xa5\xe5\x8d\x8a\xe8\xa7\x92,\xe5\x88\x86\xe5\x89\xb2', verbose_name=b'\xe6\x9c\x88\xe6\x97\xa5\xe5\x88\xa4\xe6\x96\xad', blank=True)),
                ('day_started_at', models.TimeField(default=datetime.time(0, 0), verbose_name='\u6bcf\u6708\u65e5\u5f00\u59cb\u65f6\u95f4')),
                ('day_ended_at', models.TimeField(default=datetime.time(0, 0), verbose_name='\u6bcf\u5468\u6708\u65e5\u7ed3\u675f\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u5b9e\u9a8c',
                'verbose_name_plural': '\u5b9e\u9a8c',
            },
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
    ]
