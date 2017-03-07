# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equip', '0011_auto_20150914_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipsuit',
            name='name',
            field=models.CharField(default=b'', max_length=200, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='equipsuit',
            name='nameId',
            field=models.CharField(default=b'', max_length=200, verbose_name='nameId'),
        ),
    ]
