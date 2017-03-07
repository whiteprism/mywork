# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skill', '0003_skilllevel_powerrank'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='targetHeroIds_int',
            field=models.CharField(default=0, max_length=200, verbose_name='\u5723\u7269\u6280\u80fd\u76ee\u6807\u82f1\u96c4\u5217\u8868'),
        ),
    ]
