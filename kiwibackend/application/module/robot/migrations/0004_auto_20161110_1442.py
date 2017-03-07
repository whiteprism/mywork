# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robot', '0003_robot_powerrank'),
    ]

    operations = [
        migrations.AddField(
            model_name='robot',
            name='cityLevel',
            field=models.IntegerField(default=0, verbose_name='\u4e3b\u57ce\u7b49\u7ea7'),
        ),
        migrations.AddField(
            model_name='robot',
            name='towerLevel',
            field=models.IntegerField(default=0, verbose_name='\u9632\u5fa1\u5854\u7b49\u7ea7'),
        ),
    ]
