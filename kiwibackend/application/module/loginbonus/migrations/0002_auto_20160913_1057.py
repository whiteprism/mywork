# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginbonus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginbonus',
            name='box_img',
            field=models.CharField(default=0, max_length=100, verbose_name='\u5b9d\u7bb1\u56fe\u96c6'),
        ),
        migrations.AddField(
            model_name='loginbonus',
            name='box_precent',
            field=models.IntegerField(default=0, verbose_name='\u4f4d\u7f6e'),
        ),
        migrations.AddField(
            model_name='loginbonus',
            name='box_rewards_int',
            field=models.CharField(default=0, max_length=100, verbose_name='\u5956\u52b1ID'),
        ),
    ]
