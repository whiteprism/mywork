# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equip', '0003_auto_20150908_1027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equip',
            name='gemAttrList_float',
        ),
        migrations.RemoveField(
            model_name='equip',
            name='gemList_int',
        ),
        migrations.RemoveField(
            model_name='equip',
            name='gemSlots',
        ),
    ]
