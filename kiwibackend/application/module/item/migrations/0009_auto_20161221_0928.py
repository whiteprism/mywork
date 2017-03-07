# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0008_towerstore'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ItemReward',
        ),
        migrations.DeleteModel(
            name='ItemSuit',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='getRewards_int',
            new_name='rewardIds_str',
        ),
    ]
