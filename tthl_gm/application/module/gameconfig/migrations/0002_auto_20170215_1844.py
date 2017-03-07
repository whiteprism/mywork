# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameconfig', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gamefunc',
            options={'verbose_name': '\u529f\u80fd', 'verbose_name_plural': '\u529f\u80fd'},
        ),
        migrations.AlterModelOptions(
            name='gamemodel',
            options={'ordering': ['-sort'], 'verbose_name': '\u6a21\u5757', 'verbose_name_plural': '\u6a21\u5757'},
        ),
        migrations.AddField(
            model_name='gamemodel',
            name='tag',
            field=models.CharField(default=1, max_length=20, verbose_name='\u6a21\u5757tag'),
            preserve_default=False,
        ),
    ]
