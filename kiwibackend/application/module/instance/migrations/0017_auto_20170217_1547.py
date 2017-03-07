# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0016_elementtowerlevel_nameid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='raidlevelconf',
            old_name='count_int',
            new_name='count_float',
        ),
        migrations.RenameField(
            model_name='raidlevelconf',
            old_name='minCount_int',
            new_name='minCount_float',
        ),
    ]
