# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='diamond',
        ),
        migrations.RemoveField(
            model_name='item',
            name='exp',
        ),
        migrations.RemoveField(
            model_name='item',
            name='gold',
        ),
        migrations.RemoveField(
            model_name='item',
            name='power',
        ),
        migrations.RemoveField(
            model_name='item',
            name='sp',
        ),
        migrations.RemoveField(
            model_name='item',
            name='waravoidTime',
        ),
        migrations.AddField(
            model_name='item',
            name='number',
            field=models.IntegerField(default=0, verbose_name='\u6570\u91cf'),
        ),
    ]
