# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offlinebonus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offlinebonusbase',
            name='day_add',
            field=models.IntegerField(default=0, verbose_name='\u79bb\u7ebf\u5929\u6570\u52a0\u6210'),
        ),
        migrations.AlterField(
            model_name='offlinebonusbase',
            name='lev_add',
            field=models.IntegerField(default=0, verbose_name='\u7b49\u7ea7\u52a0\u6210'),
        ),
    ]
