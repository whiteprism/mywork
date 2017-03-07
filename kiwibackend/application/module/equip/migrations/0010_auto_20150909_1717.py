# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equip', '0009_remove_equiprefine_goldcost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipattribute',
            name='initValue',
        ),
        migrations.AddField(
            model_name='equipattribute',
            name='enhanceInitValue',
            field=models.FloatField(default=0, verbose_name='\u5f3a\u5316\u521d\u59cb\u503c'),
        ),
        migrations.AddField(
            model_name='equipattribute',
            name='refineInitValue',
            field=models.FloatField(default=0, verbose_name='\u7cbe\u70bc\u521d\u59cb\u503c'),
        ),
    ]
