# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hero', '0006_auto_20170112_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='warrior',
            name='maxCount',
            field=models.IntegerField(default=0, verbose_name='\u6700\u5927\u6295\u653e\u6570\u91cf'),
        ),
    ]
