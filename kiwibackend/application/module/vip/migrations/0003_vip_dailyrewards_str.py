# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vip', '0002_vip_resetpvpcount'),
    ]

    operations = [
        migrations.AddField(
            model_name='vip',
            name='dailyRewards_str',
            field=models.CharField(default=b'', max_length=200, verbose_name='\u6bcf\u65e5\u767b\u9646\u5956\u52b1'),
        ),
    ]
