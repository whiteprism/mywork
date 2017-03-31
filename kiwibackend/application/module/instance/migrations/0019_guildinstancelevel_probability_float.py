# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0018_guildinstancelevel_guildlevellimit'),
    ]

    operations = [
        migrations.AddField(
            model_name='guildinstancelevel',
            name='probability_float',
            field=models.CharField(default=b'', max_length=100, verbose_name='\u6389\u843d\u6982\u7387'),
        ),
    ]
