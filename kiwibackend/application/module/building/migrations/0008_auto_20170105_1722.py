# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0007_auto_20170105_1600'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buildingfragment',
            name='removeRewardIds_str',
        ),
        migrations.AddField(
            model_name='building',
            name='canRemove',
            field=models.BooleanField(default=0, verbose_name='\u662f\u5426\u53ef\u4ee5\u88ab\u62c6\u9664'),
        ),
        migrations.AddField(
            model_name='building',
            name='removeRewardIds_str',
            field=models.CharField(default=b'', max_length=200, verbose_name='\u8fd4\u8fd8\u6570\u91cf'),
        ),
    ]
