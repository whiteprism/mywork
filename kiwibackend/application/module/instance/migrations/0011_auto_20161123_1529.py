# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0010_elementtowerinstance_descriptionid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elementtowerinstance',
            name='enemyIds_int',
            field=models.CharField(default=b'', max_length=500, verbose_name='\u654c\u519b\u9635\u5bb9ID'),
        ),
        migrations.AlterField(
            model_name='elementtowerinstance',
            name='rewardIds_str',
            field=models.CharField(default=b'', max_length=500, verbose_name='\u5956\u52b1ID'),
        ),
        migrations.AlterField(
            model_name='elementtowerinstance',
            name='zoneIDs_int',
            field=models.CharField(default=b'', max_length=500, verbose_name='zone ID'),
        ),
    ]
