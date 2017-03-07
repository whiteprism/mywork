# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attr',
            name='enumId',
            field=models.IntegerField(default=0, verbose_name='\u679a\u4e3eID'),
        ),
    ]
