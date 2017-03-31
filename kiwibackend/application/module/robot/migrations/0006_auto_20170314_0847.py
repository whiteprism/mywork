# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robot', '0005_auto_20170209_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='robot',
            name='siegeGold',
            field=models.IntegerField(default=0, verbose_name='\u653b\u57ce\u6218\u91d1\u5e01'),
        ),
        migrations.AddField(
            model_name='robot',
            name='siegeWood',
            field=models.IntegerField(default=0, verbose_name='\u653b\u57ce\u6218\u6728\u6750'),
        ),
    ]
