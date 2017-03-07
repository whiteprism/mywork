# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0004_auto_20161027_1004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guildinstancelevel',
            name='powerCost',
        ),
        migrations.AddField(
            model_name='guildinstancelevel',
            name='diamondCost',
            field=models.IntegerField(default=0, verbose_name='\u6d88\u8017\u94bb\u77f3'),
        ),
    ]
