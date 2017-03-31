# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hero', '0008_auto_20170120_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='warrior',
            name='attackType',
            field=models.IntegerField(default=0, verbose_name='\u653b\u51fb\u7c7b\u578b'),
        ),
    ]
