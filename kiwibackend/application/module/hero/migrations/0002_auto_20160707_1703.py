# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hero', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hero',
            old_name='collectionRecoverEnergy',
            new_name='hurtToEnergy',
        ),
    ]
