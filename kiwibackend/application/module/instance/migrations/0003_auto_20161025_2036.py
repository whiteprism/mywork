# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0002_auto_20161025_2030'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guildinstancelevel',
            old_name='aucRewardId_int',
            new_name='aucRewardIds_int',
        ),
    ]
