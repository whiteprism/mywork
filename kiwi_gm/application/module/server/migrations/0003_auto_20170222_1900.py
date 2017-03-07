# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_auto_20170222_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serverinfo',
            name='zone_name',
            field=models.CharField(max_length=30, verbose_name='\u533a\u57df\u540d\u79f0'),
        ),
    ]
