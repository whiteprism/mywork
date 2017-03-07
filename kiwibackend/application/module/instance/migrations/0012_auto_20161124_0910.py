# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0011_auto_20161123_1529'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SpaceTimeReward',
        ),
        migrations.DeleteModel(
            name='SpaceTimeRewardDetail',
        ),
    ]
