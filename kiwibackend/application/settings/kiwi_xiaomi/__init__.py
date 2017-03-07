# -*- coding: utf-8 -*-

from settings.kiwi import *     # 全局配置
from server_config import *     # 单个服务器配置

from mongoengine import connect, register_connection

DEBUG = True

import logging.config
logging.config.fileConfig("%s/settings/%s/logging_config.conf" % (ROOT_PATH, SERVER_NAME))

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
TEMPLATE_DIRS = (
   ROOT_PATH + '/website/mobile/templates/',
)
OPENSOCIAL_DEBUG = True
OPENSOCIAL_SANDBOX = True
OPENSOCIAL_SMARTPHONE_DEBUG = True
OPENSOCIAL_DEBUG_USER_ID = 1113#1000010
ENABLE_REDIS_CACHE = False
OPEN_TUTORIAL = True
OPEN_PAYMENT = False
VIP_INFO = {'buyRewardLevel':[], 'chargeCount':1000, 'vipLevel': 5}
DIAMOND = 1000
