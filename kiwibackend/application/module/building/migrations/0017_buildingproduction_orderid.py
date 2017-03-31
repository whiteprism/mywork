# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0016_auto_20170307_0915'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildingproduction',
            name='orderId',
            field=models.IntegerField(default=0, verbose_name='\u663e\u793a\u987a\u5e8f'),
        ),
    ]
