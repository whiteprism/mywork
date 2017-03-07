# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0003_buildinggoldhand'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buildingradar',
            old_name='building',
            new_name='building_id',
        ),
        migrations.RenameField(
            model_name='buildingresourceprotected',
            old_name='building',
            new_name='building_id',
        ),
        migrations.RemoveField(
            model_name='buildinggolden',
            name='building',
        ),
        migrations.RemoveField(
            model_name='buildingproduction',
            name='building',
        ),
        migrations.RemoveField(
            model_name='buildingupgrade',
            name='building',
        ),
        migrations.AddField(
            model_name='buildinggolden',
            name='building_id',
            field=models.IntegerField(default=0, verbose_name='\u5efa\u7b51ID'),
        ),
        migrations.AddField(
            model_name='buildingproduction',
            name='building_id',
            field=models.IntegerField(default=0, verbose_name='\u5efa\u7b51ID'),
        ),
        migrations.AddField(
            model_name='buildingupgrade',
            name='building_id',
            field=models.IntegerField(default=0, verbose_name='\u5efa\u7b51ID'),
        ),
    ]
