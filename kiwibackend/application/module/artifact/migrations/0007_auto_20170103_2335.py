# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artifact', '0006_auto_20161109_1117'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ArtifactFragmentGrabProb',
        ),
        migrations.RemoveField(
            model_name='artifact',
            name='composeFragmentIds_int',
        ),
        migrations.RemoveField(
            model_name='artifact',
            name='heroTypeList_int',
        ),
        migrations.RemoveField(
            model_name='artifactfragment',
            name='pos',
        ),
        migrations.RemoveField(
            model_name='artifactrefine',
            name='artifactCount',
        ),
    ]
