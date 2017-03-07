# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vip', '0003_vip_dailyrewards_str'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vip',
            name='timeGateCount',
            field=models.IntegerField(default=0, verbose_name='\u5143\u7d20\u4e4b\u5854'),
        ),
        migrations.AlterField(
            model_name='vip',
            name='titanCount',
            field=models.IntegerField(default=0, verbose_name='\u4e0a\u53e4\u9057\u8ff9'),
        ),
    ]
