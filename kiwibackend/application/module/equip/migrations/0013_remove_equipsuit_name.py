# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equip', '0012_auto_20151024_1046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipsuit',
            name='name',
        ),
    ]
