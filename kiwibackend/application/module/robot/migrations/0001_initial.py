# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Robot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.IntegerField(default=0, verbose_name='\u673a\u5668\u4eba\u7b49\u7ea7')),
                ('heroes_int', models.CharField(default=b'', max_length=200, verbose_name='\u673a\u5668\u4eba\u82f1\u96c4')),
                ('heroLevels_int', models.CharField(default=b'', max_length=200, verbose_name='\u82f1\u96c4\u7b49\u7ea7')),
                ('heroUpgrades_int', models.CharField(default=b'', max_length=200, verbose_name='\u82f1\u96c4\u9636\u6bb5')),
                ('heroStars_int', models.CharField(default=b'', max_length=200, verbose_name='\u82f1\u96c4\u661f\u7ea7')),
                ('heroPoses_int', models.CharField(default=b'', max_length=200, verbose_name='\u82f1\u96c4\u4f4d\u7f6e')),
                ('heroSkillLevels_int', models.CharField(default=b'', max_length=200, verbose_name='\u82f1\u96c4\u6280\u80fd\u7b49\u7ea7')),
                ('equipLevel', models.IntegerField(default=0, verbose_name='\u88c5\u5907\u7b49\u7ea7')),
                ('equipUpgrade', models.IntegerField(default=0, verbose_name='\u88c5\u5907\u9636\u7ea7')),
            ],
        ),
    ]
