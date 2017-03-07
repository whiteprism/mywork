# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0011_sevendaystask_showid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sevendayshalfprice',
            name='count',
        ),
        migrations.RemoveField(
            model_name='sevendayshalfprice',
            name='iconId',
        ),
        migrations.RemoveField(
            model_name='sevendayshalfprice',
            name='itemNameMul',
        ),
        migrations.RemoveField(
            model_name='sevendayshalfprice',
            name='itemType',
        ),
        migrations.RemoveField(
            model_name='sevendayshalfprice',
            name='suitId',
        ),
        migrations.AddField(
            model_name='sevendayshalfprice',
            name='rewardId',
            field=models.CharField(default=b'', max_length=200, verbose_name='\u5956\u52b1'),
        ),
    ]
