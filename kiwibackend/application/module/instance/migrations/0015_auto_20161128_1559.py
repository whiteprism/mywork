# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0014_auto_20161128_1542'),
    ]

    operations = [
        migrations.RenameField(
            model_name='elementtowerlevel',
            old_name='zoneIDs_str',
            new_name='zoneIDs_int',
        ),
    ]
