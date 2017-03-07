# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0007_sevendayshalfprice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sevendayshalfprice',
            name='itemName',
        ),
        migrations.AddField(
            model_name='sevendayshalfprice',
            name='iconId',
            field=models.IntegerField(default=0, verbose_name='\u5934\u50cf'),
        ),
    ]
