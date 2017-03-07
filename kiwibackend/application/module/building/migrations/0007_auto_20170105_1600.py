# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0006_auto_20170105_0939'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buildingfragment',
            name='composeCount',
        ),
        migrations.AlterField(
            model_name='buildingfragment',
            name='removeRewardIds_str',
            field=models.CharField(default=b'', max_length=200, verbose_name='\u8fd4\u8fd8\u6570\u91cf'),
        ),
    ]
