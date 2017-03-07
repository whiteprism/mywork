# -*- coding: utf-8 -*-

from settings.kiwi import *
from server_config import *

from mongoengine import connect, register_connection
import logging.config
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# ROOT_PATH = os.path.join(os.path.dirname(__file__),'..')
logging.config.fileConfig("%s/settings/snn/logging_config.conf" % ROOT_PATH)


# MYSQL_IP="192.168.1.58"
# MYSQL_PORT=3306
# MYSQL_USER="kiwi"
# MYSQL_PASSWD="kiwi"
# MYSQL_DATABASE_NAME="kiwi_xsf"
#
# MONGO_IP="192.168.1.58"
# MONGO_PORT=10000
# MONGO_DB_NAME="kiwi"
#
# REDIS_IP="192.168.1.58"
# REDIS_PORT=6379
# SERVERID=1
# URL="192.168.1.58:1999"
print MONGO_DB_NAME, MONGO_IP, MONGO_PORT

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
OPENSOCIAL_DEBUG = True
OPENSOCIAL_SANDBOX = True
OPENSOCIAL_SMARTPHONE_DEBUG = True
OPENSOCIAL_DEBUG_USER_ID = 1113#1000010
KVS_BASE_NAME = "KIWI" #kiwi
ENABLE_REDIS_CACHE = False
DOMAIN_URL = URL
TEMPLATE_DIRS = (
   ROOT_PATH + '/website/mobile/templates/',
)
#DEBUG = False
def yoyprint(message):
#    pass
    print message
__builtins__["yoyprint"]  = yoyprint
OPEN_TUTORIAL = False
DEBUG = True

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
