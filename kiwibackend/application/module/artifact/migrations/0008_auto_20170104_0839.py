# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artifact', '0007_auto_20170103_2335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artifact',
            name='skillId',
        ),
        migrations.AddField(
            model_name='artifact',
            name='skillIds_int',
            field=models.CharField(default=0, max_length=200, verbose_name='\u968f\u673a\u6280\u80fd\u5217\u8868'),
        ),
        migrations.AddField(
            model_name='artifactfragment',
            name='composeCount',
            field=models.IntegerField(default=0, verbose_name='\u5408\u6210\u6570\u91cf'),
        ),
    ]
