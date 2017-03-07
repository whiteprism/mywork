# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pvp', '0004_siegeattactsoldierinfo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SiegeAttactSoldierInfo',
        ),
    ]
