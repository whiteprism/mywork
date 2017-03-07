# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_auto_20150928_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailytask',
            name='buildingId',
            field=models.IntegerField(default=0, verbose_name='\u5165\u53e3\u5efa\u7b51'),
        ),
        migrations.AddField(
            model_name='task',
            name='buildingId',
            field=models.IntegerField(default=0, verbose_name='\u5165\u53e3\u5efa\u7b51'),
        ),
    ]
