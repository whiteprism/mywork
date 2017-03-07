# -*- coding: utf-8 -*-
import os
from settings.base import *

DEBUG = True

#HTML5_DEBUG = True
import logging.config
logging.config.fileConfig("%s/settings/logging_config.conf" % ROOT_PATH)


TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh-hans'

import syslog
ACTION_LOG = {
    'LOG_NAME' : 'tthl_gm',
    'FACILITY' : syslog.LOG_LOCAL5,
    'PRIORITY' : syslog.LOG_INFO,
}

# BROKER_URL = 'redis://localhost:6500/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6500/0'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'

# CELERY_REDIS_SCHEDULER_URL = "redis://localhost:6500/0"
# CELERY_REDIS_SCHEDULER_KEY_PREFIX = 'celery-beat'
# CELERY_TIMEZONE = "Asia/Shanghai"
# CELERYBEAT_MAX_LOOP_INTERVAL = 30

# from celery import Celery
# CELERY_APP = Celery('celery_app')
# CELERY_APP.autodiscover_tasks(lambda: INSTALLED_APPS)
# CELERY_APP.config_from_object('django.conf:settings')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tthl_gm',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    },
}

BATCH_LOG_DIR = '/tmp/'
SITE_DOMAIN = ''
