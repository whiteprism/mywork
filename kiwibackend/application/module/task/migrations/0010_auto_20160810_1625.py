# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0009_sevendayshalfprice_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sevendayshalfprice',
            name='limitDay',
        ),
        migrations.AddField(
            model_name='sevendayshalfprice',
            name='suitId',
            field=models.IntegerField(default=0, verbose_name='\u5957\u88c5\uff29\uff44'),
        ),
    ]
