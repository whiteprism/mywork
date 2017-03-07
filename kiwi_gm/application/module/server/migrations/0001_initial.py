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
                ('name', models.CharField(unique=True, max_length=20, verbose_name='\u670d\u52a1\u5668\u540d\u79f0')),
                ('url', models.CharField(max_length=100, null=True, verbose_name='\u8fde\u63a5\u5730\u5740', blank=True)),
            ],
        ),
    ]
