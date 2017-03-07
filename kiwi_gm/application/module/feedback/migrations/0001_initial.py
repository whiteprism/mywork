# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserFeedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField(default=b'', max_length=2000)),
                ('send_time', models.DateTimeField()),
                ('response_flag', models.BooleanField(default=False)),
            ],
        ),
    ]
