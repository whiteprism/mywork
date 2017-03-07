# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equip', '0002_auto_20150908_0953'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equip',
            name='unBindCostDiamond',
        ),
        migrations.RemoveField(
            model_name='equip',
            name='upgradeAttrList_int',
        ),
        migrations.RemoveField(
            model_name='equip',
            name='upgradeEquipId',
        ),
    ]
