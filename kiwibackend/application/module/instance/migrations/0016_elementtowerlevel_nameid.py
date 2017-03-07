# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0015_auto_20161128_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='elementtowerlevel',
            name='nameId',
            field=models.CharField(default=b'', max_length=200, verbose_name='\u540d\u5b57id'),
        ),
    ]
