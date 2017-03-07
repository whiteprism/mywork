# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gashapon', '0002_auto_20150906_0843'),
    ]

    operations = [
        migrations.AddField(
            model_name='tavern',
            name='rewardId',
            field=models.CharField(default='', max_length=255, verbose_name=b'\xe5\x8d\x95\xe6\x8a\xbd\xe5\xa5\x96\xe5\x8a\xb1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tavern',
            name='tenRewardId',
            field=models.CharField(default='', max_length=255, verbose_name=b'\xe5\x8d\x81\xe8\xbf\x9e\xe6\x8a\xbd\xe5\xa5\x96\xe5\x8a\xb1'),
            preserve_default=False,
        ),
    ]
