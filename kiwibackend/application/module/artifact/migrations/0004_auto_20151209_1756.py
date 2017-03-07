# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artifact', '0003_auto_20151209_1606'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artifact',
            name='searchDifficuty_int',
        ),
        migrations.RemoveField(
            model_name='artifact',
            name='searchInstances_int',
        ),
    ]
