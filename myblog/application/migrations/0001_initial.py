# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='blogPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=30, verbose_name='\u6807\u9898')),
                ('content', models.TextField(default='', max_length=3000)),
                ('time', models.DateTimeField(default=datetime.datetime(2017, 3, 1, 8, 55, 40, 193653))),
            ],
            options={
                'ordering': ['-time'],
            },
        ),
    ]
