# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='serverinfo',
            name='code',
            field=models.CharField(default=b'', max_length=30, verbose_name='\u670d\u52a1\u5668\u4ee3\u53f7'),
        ),
        migrations.AddField(
            model_name='serverinfo',
            name='open_at',
            field=models.CharField(default=123, max_length=200, verbose_name='\u5f00\u670d\u65f6\u95f4'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='serverinfo',
            name='status_id',
            field=models.IntegerField(default=1, verbose_name='\u670d\u52a1\u5668\u72b6\u6001ID'),
        ),
        migrations.AddField(
            model_name='serverinfo',
            name='status_text',
            field=models.CharField(default=1, max_length=20, verbose_name='\u670d\u52a1\u5668\u72b6\u6001\u63cf\u8ff0'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='serverinfo',
            name='zone_id',
            field=models.IntegerField(default=1, verbose_name='\u533a\u57dfID'),
        ),
        migrations.AddField(
            model_name='serverinfo',
            name='zone_name',
            field=models.CharField(default=1, unique=True, max_length=20, verbose_name='\u533a\u57df\u540d\u79f0'),
            preserve_default=False,
        ),
    ]
