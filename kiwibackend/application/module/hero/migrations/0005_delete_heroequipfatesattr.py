# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hero', '0004_auto_20160810_1437'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HeroEquipFatesAttr',
        ),
    ]
