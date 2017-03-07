# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0010_building_buildingplantid'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BuildingPlant',
        ),
        migrations.RemoveField(
            model_name='building',
            name='buildingPlantId',
        ),
    ]
