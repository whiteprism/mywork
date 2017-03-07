# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equip', '0005_auto_20150908_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardequipinfo',
            name='pos5_int',
            field=models.CharField(default=0, max_length=300, verbose_name='\u4f4d\u7f6e5'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cardequipinfo',
            name='pos6_int',
            field=models.CharField(default=0, max_length=300, verbose_name='\u4f4d\u7f6e6'),
            preserve_default=False,
        ),
    ]
