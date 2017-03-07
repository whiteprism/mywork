# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('levelconf', '0002_levelconf_battlepoint'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='levelconf',
            name='heroUpgradeLimit',
        ),
    ]
