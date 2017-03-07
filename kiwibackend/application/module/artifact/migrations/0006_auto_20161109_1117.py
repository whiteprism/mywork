# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artifact', '0005_artifacefragmentgrabprob'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ArtifaceFragmentGrabProb',
            new_name='ArtifactFragmentGrabProb',
        ),
    ]
