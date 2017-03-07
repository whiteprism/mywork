# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginbonus', '0002_auto_20160913_1057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loginbonus',
            name='box_img',
        ),
        migrations.RemoveField(
            model_name='loginbonus',
            name='box_precent',
        ),
        migrations.RemoveField(
            model_name='loginbonus',
            name='box_rewards_int',
        ),
    ]
