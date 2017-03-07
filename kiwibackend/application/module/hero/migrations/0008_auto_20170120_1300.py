# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hero', '0007_warrior_maxcount'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HeroTrain',
        ),
        migrations.RemoveField(
            model_name='hero',
            name='trainAttackMax',
        ),
        migrations.RemoveField(
            model_name='hero',
            name='trainHpMax',
        ),
        migrations.RemoveField(
            model_name='hero',
            name='trainMagicArmorMax',
        ),
        migrations.RemoveField(
            model_name='hero',
            name='trainPhysicalArmorMax',
        ),
    ]
