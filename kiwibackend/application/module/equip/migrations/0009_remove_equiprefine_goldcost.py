# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equip', '0008_auto_20150909_0935'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equiprefine',
            name='goldCost',
        ),
    ]
