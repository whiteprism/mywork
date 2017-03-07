# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='robot',
            name='score',
            field=models.IntegerField(default=0, verbose_name='\u5206\u6570'),
        ),
    ]
