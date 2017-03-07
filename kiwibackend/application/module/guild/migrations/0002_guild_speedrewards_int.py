# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guild', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='guild',
            name='speedRewards_int',
            field=models.CharField(default=b'', max_length=200, verbose_name='\u73a9\u5bb6\u4e4b\u95f4\u52a0\u901f\u600e\u9001\u9053\u5177'),
        ),
    ]
