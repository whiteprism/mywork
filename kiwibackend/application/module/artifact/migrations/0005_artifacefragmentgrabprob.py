# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import submodule.fanyoy.redis.static
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('artifact', '0004_auto_20151209_1756'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtifaceFragmentGrabProb',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('robotProb', models.IntegerField(default=0, verbose_name='\u673a\u5668\u4eba\u5355\u6b21\u62a2\u593a\u6982\u7387')),
                ('playerProb', models.IntegerField(default=0, verbose_name='\u771f\u4eba\u5355\u6b21\u62a2\u593a\u6982\u7387')),
                ('robotTenProbs_int', models.CharField(default=b'', max_length=200, verbose_name='\u673a\u5668\u4eba10\u6b21\u62a2\u593a\u6982\u7387')),
            ],
            bases=(models.Model, submodule.fanyoy.redis.static.StaticDataRedisHandler, common.models.CommonStaticModels),
        ),
    ]
