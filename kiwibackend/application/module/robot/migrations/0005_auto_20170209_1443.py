# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robot', '0004_auto_20161110_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='robot',
            name='siegeSoldierIds_int',
            field=models.CharField(default=b'', max_length=200, verbose_name='\u57ce\u5899\u5175\u7ad9\u4f4d'),
        ),
        migrations.AddField(
            model_name='robot',
            name='siegeSoldierLevels_int',
            field=models.CharField(default=b'', max_length=200, verbose_name='\u57ce\u5899\u5175\u7b49\u7ea7'),
        ),
    ]
