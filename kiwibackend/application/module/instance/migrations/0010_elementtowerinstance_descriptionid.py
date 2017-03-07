# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0009_auto_20161123_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='elementtowerinstance',
            name='descriptionId',
            field=models.CharField(default=b'', max_length=50, verbose_name='\u63cf\u8ff0'),
        ),
    ]
