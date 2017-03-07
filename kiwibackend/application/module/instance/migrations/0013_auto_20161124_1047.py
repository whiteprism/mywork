# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0012_auto_20161124_0910'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='elementtowerinstance',
            name='enemyIds_int',
        ),
        migrations.RemoveField(
            model_name='elementtowerinstance',
            name='zoneIDs_int',
        ),
        migrations.AddField(
            model_name='elementtowerlevel',
            name='enemyId',
            field=models.IntegerField(default=0, verbose_name='\u654c\u519b\u9635\u5bb9ID'),
        ),
        migrations.AddField(
            model_name='elementtowerlevel',
            name='zoneID',
            field=models.IntegerField(default=0, verbose_name='zone ID'),
        ),
    ]
