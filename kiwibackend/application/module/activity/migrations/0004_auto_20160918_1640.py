# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0003_auto_20160918_1432'),
    ]

    operations = [
        migrations.RenameField(
            model_name='giftpackage',
            old_name='boxImg',
            new_name='boxImgs_str',
        ),
    ]
