# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0006_itemsuit_suittoitemid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemsuit',
            name='iconId',
            field=models.CharField(default=b'', max_length=500, verbose_name='\u5b9d\u7bb1\u56fe\u6807'),
        ),
    ]
