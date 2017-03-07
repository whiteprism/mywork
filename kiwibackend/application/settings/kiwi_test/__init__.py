# -*- coding: utf-8 -*-

from settings.kiwi import *
from mongoengine import connect, register_connection
DEBUG = True

import logging.config
logging.config.fileConfig("%s/settings/kiwi_test/logging_config.conf" % ROOT_PATH)

connect('kiwi_test', host="127.0.0.1",  port=27018, username='', password='')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kiwi_test',
        'USER': 'kiwi',
        'PASSWORD': 'kiwi',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    },
    'read': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kiwi_test',
        'USER': 'kiwi',
        'PASSWORD': 'kiwi',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

REDIS_CACHES = { 
    'increment': {
        'host': '127.0.0.1',
        'port': 6382
    },
    'default': [{
        'host': '127.0.0.1',
        'port': 6382
    }],
    'player': [{
        'host': '127.0.0.1',
        'port': 6382
    }]
}
CACHES = { 
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '%s:%s' % ("127.0.0.1", 6382),
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
KVS_BASE_NAME = "KIWI_TEST" #kiwi
SERVERID = 6
ENABLE_REDIS_CACHE = False
DOMAIN_URL ="42.121.66.154:2001"
TEMPLATE_DIRS = (
   ROOT_PATH + '/website/mobile/templates/',
)
#DEBUG = False
def yoyprint(message):
#    pass
    print message
__builtins__["yoyprint"]  = yoyprint
OPEN_TUTORIAL = False
