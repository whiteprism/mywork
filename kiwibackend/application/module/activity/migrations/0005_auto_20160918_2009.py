# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0004_auto_20160918_1640'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='beginTime',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='endTime',
        ),
        migrations.AddField(
            model_name='activity',
            name='experiment_name',
            field=models.CharField(default=b'', max_length=100, verbose_name='\u5b9e\u9a8c\u540d'),
        ),
    ]
