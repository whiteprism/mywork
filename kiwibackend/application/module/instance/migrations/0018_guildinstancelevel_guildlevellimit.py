# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0017_auto_20170217_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='guildinstancelevel',
            name='guildLevelLimit',
            field=models.IntegerField(default=0, verbose_name='\u5f00\u542f\u526f\u672c\u7b49\u7ea7'),
        ),
    ]
