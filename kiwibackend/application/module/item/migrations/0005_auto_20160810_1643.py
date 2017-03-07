# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0004_auto_20160810_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemsuit',
            name='boxNameId',
            field=models.CharField(default=b'', max_length=300, verbose_name='\u5b9d\u7bb1id'),
        ),
    ]
