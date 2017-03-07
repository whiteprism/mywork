# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arenashop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='arenashop',
            name='type',
            field=models.IntegerField(default=0, verbose_name='\u663e\u793a\u7c7b\u522b'),
        ),
    ]
