# -*- coding: utf-8 -*-
import redis
#from .client import get_client
from django.conf import settings
import random
import time
from module.utils import unixtime_to_datetime
try:
    import cPickle as pickle
except:
    import pickle

DEFAULT_DB = "default"
DEFAULT_DYNAMIC_DB = "player"

class HandlerError(Exception):
    pass


class RedisHandlerBase(object):
    """
    redis 基础操作
    """

    def __init__(self, *args, **kwargs):
        """
        获取redis链接
        """
        pass

    @classmethod
    def get_client(cls, config):
        if "password" in config:
            pool = redis.ConnectionPool(host=config["host"], port=config["port"], password=config["password"]) 
        else:
            pool = redis.ConnectionPool(host=config["host"], port=config["port"]) 
        return redis.Redis(connection_pool=pool) 

    @classmethod
    def get_kvs_key(cls, key="ALL", sec_key=None):
        """
        获取KVS key
        """
        if sec_key:
            #print "%s:%s:%s:%s" % (settings.KVS_BASE_NAME, cls.__name__, key, sec_key)
            return "%s:%s:%s:%s" % (settings.KVS_BASE_NAME, cls.__name__, key, sec_key)
        else:
            #print "%s:%s:%s" % (settings.KVS_BASE_NAME, cls.__name__, key)
            return "%s:%s:%s" % (settings.KVS_BASE_NAME, cls.__name__, key)
