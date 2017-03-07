# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='condition',
        ),
        migrations.AddField(
            model_name='task',
            name='condition_id',
            field=models.IntegerField(default=0, verbose_name='\u4efb\u52a1\u6761\u4ef6ID'),
        ),
    ]
