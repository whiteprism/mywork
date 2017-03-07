# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robot', '0002_robot_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='robot',
            name='powerRank',
            field=models.IntegerField(default=0, verbose_name='\u673a\u5668\u4eba\u6218\u6597\u529b'),
        ),
    ]