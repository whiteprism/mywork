# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0009_buildingplant'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='buildingPlantId',
            field=models.IntegerField(default=0, verbose_name='\u690d\u7269\u5c5e\u6027\u8868ID'),
        ),
    ]
