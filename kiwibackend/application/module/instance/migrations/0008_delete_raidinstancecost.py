# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0007_auto_20161123_1354'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RaidInstanceCost',
        ),
    ]
