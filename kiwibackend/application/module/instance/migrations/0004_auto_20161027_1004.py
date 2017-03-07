# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0003_auto_20161025_2036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guildinstancelevel',
            name='probability_float',
        ),
        migrations.AddField(
            model_name='guildinstancelevel',
            name='aucRewardMaxCount_int',
            field=models.CharField(default=b'', max_length=100, verbose_name='\u6389\u843d\u7269\u54c1\u6570\u91cf'),
        ),
    ]
