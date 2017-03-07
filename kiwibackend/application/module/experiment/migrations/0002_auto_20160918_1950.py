# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experiment',
            name='day_ended_at',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='day_started_at',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='ended_at1',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='ended_at2',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='ended_at3',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='monthdays_str',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='started_at1',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='started_at2',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='started_at3',
        ),
        migrations.AddField(
            model_name='experiment',
            name='ended_at',
            field=models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0), verbose_name='\u7ed3\u675f\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='is_alltime',
            field=models.BooleanField(default=False, verbose_name=b'\xe6\x97\xb6\xe9\x97\xb4\xe6\xae\xb5\xe6\xa3\x80\xe6\x9f\xa5'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='is_weektime',
            field=models.BooleanField(default=False, verbose_name=b'\xe6\x98\x9f\xe6\x9c\x9f\xe7\x82\xb9\xe6\xa3\x80\xe6\x9f\xa5'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='started_at',
            field=models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0), verbose_name='\u5f00\u59cb\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='valuesStr',
            field=models.TextField(help_text=b'\xe6\xa0\xb9\xe6\x8d\xae\xe5\xae\x9e\xe9\xaa\x8c\xe4\xbd\xbf\xe7\x94\xa8\xe7\x8e\xaf\xe5\xa2\x83\xe5\xae\x9a\xe4\xb9\x89DEMO:a:1,2,3[\xe5\x9b\x9e\xe8\xbd\xa6][\xe5\x9b\x9e\xe8\xbd\xa6]b:1', verbose_name=b'\xe9\x99\x84\xe5\x8a\xa0\xe5\x80\xbc', blank=True),
        ),
    ]
