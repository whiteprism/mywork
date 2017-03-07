# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vip', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vip',
            name='resetPVPCount',
            field=models.IntegerField(default=0, verbose_name='\u7ade\u6280\u573a\u91cd\u7f6e\u6b21\u6570'),
        ),
    ]
