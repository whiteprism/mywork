# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0015_auto_20170222_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildingproduction',
            name='descriptionId',
            field=models.CharField(default=b'', max_length=200, verbose_name='descriptionId'),
        ),
        migrations.AddField(
            model_name='buildingproduction',
            name='icon',
            field=models.CharField(default=b'', max_length=200, verbose_name='icon'),
        ),
        migrations.AddField(
            model_name='buildingproduction',
            name='nameId',
            field=models.CharField(default=b'', max_length=200, verbose_name='nameId'),
        ),
    ]
