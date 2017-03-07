# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equip', '0010_auto_20150909_1717'),
    ]

    operations = [
        migrations.RenameField(
            model_name='equiprefine',
            old_name='refineCost',
            new_name='refineXp',
        ),
    ]
