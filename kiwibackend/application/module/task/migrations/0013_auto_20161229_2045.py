# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0012_auto_20161221_1757'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskcondition',
            name='c1_int',
        ),
        migrations.RemoveField(
            model_name='taskcondition',
            name='c2_int',
        ),
        migrations.AddField(
            model_name='taskcondition',
            name='c1',
            field=models.IntegerField(default=0, verbose_name='condition1'),
        ),
    ]
