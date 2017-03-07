# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vip', '0004_auto_20161209_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='vip',
            name='plantCount',
            field=models.IntegerField(default=0, verbose_name='\u53ef\u5efa\u9020\u7684\u690d\u7269\u603b\u6570'),
        ),
        migrations.AddField(
            model_name='vip',
            name='statueCount',
            field=models.IntegerField(default=0, verbose_name='\u53ef\u5efa\u9020\u7684\u795e\u50cf\u603b\u6570'),
        ),
    ]
