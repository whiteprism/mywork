# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0013_auto_20161124_1047'),
    ]

    operations = [
        migrations.RenameField(
            model_name='elementtowerbuff',
            old_name='attrs_int',
            new_name='attrTypes_str',
        ),
        migrations.RemoveField(
            model_name='elementtowerlevel',
            name='zoneID',
        ),
        migrations.AddField(
            model_name='elementtowerlevel',
            name='zoneIDs_str',
            field=models.CharField(default=b'', max_length=300, verbose_name='zone ID'),
        ),
    ]
