# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skill', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skilleffect',
            name='skilllevel',
        ),
        migrations.RemoveField(
            model_name='skilleffectdetail',
            name='skill',
        ),
        migrations.RemoveField(
            model_name='skilllevel',
            name='skill',
        ),
        migrations.AddField(
            model_name='skilleffect',
            name='skilllevel_id',
            field=models.IntegerField(default=1, verbose_name='\u6280\u80fd\u7b49\u7ea7'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skilleffectdetail',
            name='skill_id',
            field=models.IntegerField(default=1, verbose_name='\u6280\u80fd'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skilllevel',
            name='skill_id',
            field=models.IntegerField(default=1, verbose_name='\u6280\u80fd'),
            preserve_default=False,
        ),
    ]
