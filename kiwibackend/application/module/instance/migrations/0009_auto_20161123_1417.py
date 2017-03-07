# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0008_delete_raidinstancecost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='elementtowerlevel',
            name='difficulty',
        ),
        migrations.AddField(
            model_name='elementtowerlevel',
            name='difficulties_int',
            field=models.CharField(default=b'', max_length=300, verbose_name='\u96be\u5ea6'),
        ),
    ]
