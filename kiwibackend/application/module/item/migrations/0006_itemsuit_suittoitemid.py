# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0005_auto_20160810_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemsuit',
            name='suitToItemId',
            field=models.IntegerField(default=0, verbose_name='\u5bf9\u5e94\u5230\u7269\u54c1\u8868\u91cc\u7684id'),
        ),
    ]
