# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GameAuth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('secret_level', models.IntegerField(default=1, verbose_name='\u6388\u6743\u7b49\u7ea7', choices=[(1, '\u666e\u901aA'), (2, '\u666e\u901aB'), (3, '\u666e\u901aC'), (4, '\u7279\u6b8aA'), (5, '\u7279\u6b8aB'), (6, '\u7279\u6b8aC')])),
                ('user', models.ForeignKey(verbose_name='\u7528\u6237', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u6743\u9650',
                'verbose_name_plural': '\u7528\u6237\u6743\u9650',
            },
        ),
        migrations.CreateModel(
            name='GameFunc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20, verbose_name='\u540d\u79f0')),
                ('url', models.CharField(max_length=100, null=True, verbose_name='\u8fde\u63a5\u5730\u5740', blank=True)),
                ('sort', models.IntegerField(default=1, verbose_name='\u6392\u5e8f')),
                ('secret_level', models.IntegerField(default=1, verbose_name='\u6388\u6743\u7b49\u7ea7', choices=[(1, '\u666e\u901aA'), (2, '\u666e\u901aB'), (3, '\u666e\u901aC'), (4, '\u7279\u6b8aA'), (5, '\u7279\u6b8aB'), (6, '\u7279\u6b8aC')])),
            ],
            options={
                'verbose_name': '\u6a21\u5757',
                'verbose_name_plural': '\u6a21\u5757',
                'default_related_name': '\u6a21\u5757',
            },
        ),
        migrations.CreateModel(
            name='GameModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20, verbose_name='\u6a21\u5757\u540d\u79f0')),
                ('url', models.CharField(max_length=100, null=True, verbose_name='\u8fde\u63a5\u5730\u5740', blank=True)),
                ('sort', models.IntegerField(default=1, verbose_name='\u6392\u5e8f')),
                ('secret_level', models.IntegerField(default=1, verbose_name='\u6388\u6743\u7b49\u7ea7', choices=[(1, '\u666e\u901aA'), (2, '\u666e\u901aB'), (3, '\u666e\u901aC'), (4, '\u7279\u6b8aA'), (5, '\u7279\u6b8aB'), (6, '\u7279\u6b8aC')])),
            ],
            options={
                'verbose_name': '\u6a21\u5757',
                'verbose_name_plural': '\u6a21\u5757',
                'default_related_name': '\u6a21\u5757',
            },
        ),
        migrations.AddField(
            model_name='gamefunc',
            name='gamemodel',
            field=models.ManyToManyField(to='gameconfig.GameModel', verbose_name='\u6a21\u5757'),
        ),
    ]
