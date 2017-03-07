# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artifact', '0002_auto_20150914_0908'),
    ]

    operations = [
        migrations.AddField(
            model_name='artifact',
            name='heroTypeList_int',
            field=models.CharField(default=b'', max_length=200, verbose_name='\u88c5\u5907\u7684\u82f1\u96c4\u7684\u7c7b\u578b'),
        ),
        migrations.AddField(
            model_name='artifact',
            name='searchDifficuty_int',
            field=models.CharField(default=b'', max_length=200, verbose_name='\u6389\u843d\u5173\u5361\u96be\u5ea6'),
        ),
        migrations.AddField(
            model_name='artifact',
            name='searchInstances_int',
            field=models.CharField(default=b'', max_length=200, verbose_name='\u6389\u843d\u5173\u5361'),
        ),
    ]
