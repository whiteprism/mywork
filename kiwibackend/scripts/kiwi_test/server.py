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

os.environ['DJANGO_SETTINGS_MODULE'] = 'application.settings.kiwi_test'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


#################### Test uWSGI Cron begin ############################
## uwsgi.add_cron(signal, minute, hour, day, month, weekday)
## uwsgi.add_timer(signal, sec)

import uwsgi

from cron_job import *

for job_id, job in enumerate(jobs):
    uwsgi.register_signal(job_id, "", job['name'])
    if len(job['time']) == 1:
        uwsgi.add_timer(job_id, job['time'][0])
    else:
        uwsgi.add_cron(job_id, job['time'][0], job['time'][1], job['time'][2], job['time'][3], job['time'][4])

#################### Test uWSGI Cron end ############################
