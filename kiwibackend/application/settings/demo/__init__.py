# -*- coding: utf-8 -*-

from settings.kiwi import *
from mongoengine import connect, register_connection
DEBUG = True

import logging.config
logging.config.fileConfig("%s/settings/demo/logging_config.conf" % ROOT_PATH)

connect('kiwi2', host="127.0.0.1",  port=27018, username='', password='')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
#        'ENGINE': 'django_mysqlpool.backends.mysqlpool',
        'NAME': 'kiwi2',
        'USER': 'kiwi',
        'PASSWORD': 'kiwi',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    },
    'read': {
        'ENGINE': 'django.db.backends.mysql',
#        'ENGINE': 'django_mysqlpool.backends.mysqlpool',
        'NAME': 'kiwi2',
        'USER': 'kiwi',
        'PASSWORD': 'kiwi',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

REDIS_CACHES = { 
    'increment': {
        'host': '127.0.0.1',
        'port': 6379
    },
    'default': [{
        'host': '127.0.0.1',
        'port': 6379
    }],
    'player': [{
        'host': '127.0.0.1',
        'port': 6379
    }]
}
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '127.0.0.1:6379' ,
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
OPENSOCIAL_DEBUG = True
OPENSOCIAL_SANDBOX = True
OPENSOCIAL_SMARTPHONE_DEBUG = True
OPENSOCIAL_DEBUG_USER_ID = 1113#1000010
KVS_BASE_NAME = "KIWI" #kiwi
SERVERID = 2
ENABLE_REDIS_CACHE = False
DOMAIN_URL ="42.121.66.154:1999"
TEMPLATE_DIRS = (
   ROOT_PATH + '/website/mobile/templates/',
)
def yoyprint(message):
#    pass
    print message
__builtins__["yoyprint"]  = yoyprint
OPEN_TUTORIAL = True
ALL_SERVERS = [0, 2]


import djcelery
djcelery.setup_loader()
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_REDIS_SCHEDULER_URL = "redis://localhost:6379/0"
CELERY_REDIS_SCHEDULER_KEY_PREFIX = 'celery-beat'
CELERY_TIMEZONE = "Asia/Shanghai"
CELERYBEAT_MAX_LOOP_INTERVAL = 30
