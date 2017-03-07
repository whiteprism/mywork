# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0002_auto_20160913_1159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activityrule',
            name='box_img',
        ),
        migrations.RemoveField(
            model_name='activityrule',
            name='box_precent',
        ),
        migrations.RemoveField(
            model_name='activityrule',
            name='box_rewards_int',
        ),
        migrations.AddField(
            model_name='giftpackage',
            name='boxImg',
            field=models.CharField(default=0, max_length=100, verbose_name='\u5b9d\u7bb1\u56fe\u96c6'),
        ),
        migrations.AddField(
            model_name='giftpackage',
            name='boxPrecent',
            field=models.IntegerField(default=0, verbose_name='\u4f4d\u7f6e'),
        ),
        migrations.AddField(
            model_name='giftpackage',
            name='boxRewards_int',
            field=models.CharField(default=0, max_length=100, verbose_name='\u5956\u52b1ID'),
        ),
    ]
