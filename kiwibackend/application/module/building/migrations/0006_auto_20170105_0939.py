# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0005_auto_20170105_0759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingattribute',
            name='maxValue',
            field=models.FloatField(default=0, verbose_name='\u6700\u5927\u503c'),
        ),
        migrations.AlterField(
            model_name='buildingattribute',
            name='minValue',
            field=models.FloatField(default=0, verbose_name='\u6700\u5c0f\u503c'),
        ),
    ]
