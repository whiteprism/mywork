# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skill', '0002_auto_20150826_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='skilllevel',
            name='powerRank',
            field=models.IntegerField(default=0, verbose_name='\u6218\u6597\u529b'),
        ),
    ]
