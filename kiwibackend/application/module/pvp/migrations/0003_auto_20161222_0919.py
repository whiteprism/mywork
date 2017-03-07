# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pvp', '0002_siegerandomnumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siegerandomnumber',
            name='number',
            field=models.FloatField(default=0, verbose_name='\u653b\u57ce\u6218\u968f\u673a\u6570'),
        ),
    ]
