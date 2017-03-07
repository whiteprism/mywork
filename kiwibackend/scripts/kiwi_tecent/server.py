# -*- mode: Python; -*-
import site
import sys
site_package_dir = ''
for p in sys.path:
    if p.endswith("site-packages"):
        site_package_dir = p

site.addsitedir(site_package_dir)

import os

paths = (
   os.path.abspath(os.path.join(os.path.dirname(__file__), '../../application/module')),
   os.path.abspath(os.path.join(os.path.dirname(__file__), '../../application/submodule')),
   os.path.abspath(os.path.join(os.path.dirname(__file__), '../../application/website')),
   os.path.abspath(os.path.join(os.path.dirname(__file__), '../../application')),
   os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')),
   )

for path in paths:
   sys.path.insert(0,path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'application.settings.kiwi_tecent'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
