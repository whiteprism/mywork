# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('levelconf', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='levelconf',
            name='battlePoint',
            field=models.IntegerField(default=0, verbose_name='\u6218\u6597\u70b9'),
        ),
    ]
