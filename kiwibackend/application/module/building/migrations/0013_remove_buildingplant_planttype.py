# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0012_auto_20170106_2258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buildingplant',
            name='plantType',
        ),
    ]
