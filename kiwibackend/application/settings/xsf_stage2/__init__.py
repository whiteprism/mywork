# -*- coding: utf-8 -*-

from settings.kiwi import *
from server_config import *
from celery import Celery

from mongoengine import connect, register_connection
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import logging.config
logging.config.fileConfig("%s/settings/xsf_stage2/logging_config.conf" % ROOT_PATH)

import djcelery
djcelery.setup_loader()
BROKER_URL = 'redis://localhost:6382/0'
BROKER_TRANSPORT = "redis"
CELERY_RESULT_BACKEND = 'redis://localhost:6382/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_REDIS_SCHEDULER_URL = "redis://localhost:6382/0"
CELERY_REDIS_SCHEDULER_KEY_PREFIX = 'celery-beat'
CELERY_TIMEZONE = "Asia/Shanghai"
CELERYBEAT_MAX_LOOP_INTERVAL = 30

CELERY_APP = Celery('celery_app')
CELERY_APP.autodiscover_tasks(lambda: INSTALLED_APPS)
CELERY_APP.config_from_object('django.conf:settings')


connect(MONGO_DB_NAME, host=MONGO_IP,  port=MONGO_PORT, username='', password='')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': MYSQL_DATABASE_NAME,
        'USER': MYSQL_USER,
        'PASSWORD': MYSQL_PASSWD,
        'HOST': MYSQL_IP,
        'PORT': MYSQL_PORT,
    },
    'read': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': MYSQL_DATABASE_NAME,
        'USER': MYSQL_USER,
        'PASSWORD': MYSQL_PASSWD,
        'HOST': MYSQL_IP,
        'PORT': MYSQL_PORT,
    }
}

REDIS_CACHES = { 
    'increment': {
        'host': "192.168.1.58",
        'port': 6382
    },
    'default': [{
        'host': "192.168.1.58",
        'port': 6382
    }],
    'player': [
        {
            'host': "192.168.1.58",
            'port': 6382
        },
    ]
}
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '%s:%s' % ("192.168.1.58", "6382"),
        'OPTIONS': {
            'DB': 1,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'timeout': 20,
            }
        },
    
    },
}




def yoyprint(message):
#    pass
    print message
__builtins__["yoyprint"]  = yoyprint
DEBUG = True
