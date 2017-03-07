# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0005_auto_20161027_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='raidlevelconf',
            name='suggestHeroIds_int',
            field=models.CharField(default=b'', max_length=1000, verbose_name='\u63a8\u8350\u4e0a\u9635\u82f1\u96c4ID'),
        ),
    ]
