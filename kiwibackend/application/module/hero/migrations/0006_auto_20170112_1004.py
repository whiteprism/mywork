# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hero', '0005_delete_heroequipfatesattr'),
    ]

    operations = [
        migrations.AddField(
            model_name='herobubble',
            name='sneerTypeMessage_str',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='herobubble',
            name='sneerTypeProperbility',
            field=models.FloatField(default=0.0),
        ),
    ]
