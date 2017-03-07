# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hero', '0003_auto_20160804_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heroequipfatesattr',
            name='equipId',
            field=models.IntegerField(default=0, verbose_name='\u88c5\u5907id'),
        ),
    ]
