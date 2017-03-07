# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guildinstancelevel',
            old_name='rewardId_int',
            new_name='aucRewardId_int',
        ),
        migrations.RemoveField(
            model_name='guildinstancelevel',
            name='count_int',
        ),
        migrations.RemoveField(
            model_name='guildinstancelevel',
            name='price_int',
        ),
    ]
