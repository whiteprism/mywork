# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_auto_20170222_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='serverinfo',
            name='gm_url',
            field=models.CharField(max_length=200, null=True, verbose_name='\u8fde\u63a5\u5730\u5740', blank=True),
        ),
        migrations.AlterField(
            model_name='serverinfo',
            name='url',
            field=models.CharField(max_length=200, null=True, verbose_name='\u8fde\u63a5\u5730\u5740', blank=True),
        ),
    ]
