# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0020_auto_20170330_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='guildinstancelevel',
            name='rewardGold',
            field=models.IntegerField(default=0, verbose_name='\u8be5\u526f\u672c\u5956\u52b1\u7684\u603b\u516c\u4f1a\u5e01'),
        ),
    ]
