# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0005_auto_20160918_2009'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='experiment_name',
            new_name='experimentName',
        ),
    ]
