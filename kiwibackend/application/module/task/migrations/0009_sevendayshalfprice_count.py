# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0008_auto_20160810_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='sevendayshalfprice',
            name='count',
            field=models.IntegerField(default=0, verbose_name='\u6570\u91cf'),
        ),
    ]
