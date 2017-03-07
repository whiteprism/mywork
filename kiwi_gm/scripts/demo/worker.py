#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 surfer <surfer@LinuxMint>
#
# Distributed under terms of the MIT license.
from __future__ import absolute_import

import os
from celery import Celery
import sys

paths = (
   os.path.abspath(os.path.join(os.path.dirname(__file__), '../../application/module')),
   os.path.abspath(os.path.join(os.path.dirname(__file__), '../../application/submodule')),
   os.path.abspath(os.path.join(os.path.dirname(__file__), '../../application/website')),
   os.path.abspath(os.path.join(os.path.dirname(__file__), '../../application')),
   os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')),
   )

for path in paths:
   sys.path.insert(0,path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings.demo')

app = Celery('celery_app')
app.config_from_object('django.conf:settings')
from django.conf import settings
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
