# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equip', '0007_auto_20150908_1548'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equip',
            name='decomposeCost',
        ),
        migrations.AddField(
            model_name='equip',
            name='decomposeRefinePoint',
            field=models.IntegerField(default=0, verbose_name='\u5206\u89e3\u83b7\u53d6\u7cbe\u70bc\u70b9'),
        ),
    ]
