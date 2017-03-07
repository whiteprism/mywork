# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equip', '0004_auto_20150908_1034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equip',
            name='gradePlus',
        ),
        migrations.RemoveField(
            model_name='equip',
            name='upgrade',
        ),
    ]
