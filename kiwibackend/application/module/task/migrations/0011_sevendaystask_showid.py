# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0010_auto_20160810_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='sevendaystask',
            name='showId',
            field=models.IntegerField(default=0, verbose_name='\u7edf\u8ba1'),
        ),
    ]
