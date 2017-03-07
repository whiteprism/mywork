# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gashapon', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gashaponprobability',
            name='rarity',
            field=models.SmallIntegerField(verbose_name='\u5206\u7c7b'),
        ),
        migrations.AlterField(
            model_name='gashaponrarityprobability',
            name='rarity',
            field=models.SmallIntegerField(default=1, verbose_name='\u5206\u7c7b'),
        ),
    ]
