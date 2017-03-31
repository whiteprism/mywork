# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0019_guildinstancelevel_probability_float'),
    ]

    operations = [
        migrations.RenameField(
            model_name='elementtowerlevel',
            old_name='difficulties_int',
            new_name='difficulties_float',
        ),
    ]
