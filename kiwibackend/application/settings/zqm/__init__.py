# -*- coding: utf-8 -*-

from settings.kiwi import *
from server_config import *

from mongoengine import connect, register_connection
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import logging.config
logging.config.fileConfig("%s/settings/zqm/logging_config.conf" % ROOT_PATH)

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
        'host': REDIS_IP,
        'port': REDIS_PORT
    },
    'default': [{
        'host': REDIS_IP,
        'port': REDIS_PORT
    }],
    'player': [{
        'host': REDIS_IP,
        'port': REDIS_PORT
        }]
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '%s:%s' % (REDIS_IP, REDIS_PORT),
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
