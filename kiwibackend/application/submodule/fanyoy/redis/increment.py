# -*- coding: utf-8 -*-
import redis
from base import RedisHandlerBase
from django.conf import settings
#INIT_VALUE = 10**10
INCREMENT = 1 

class IncrmentId(RedisHandlerBase):
    """
    维护自增ID
    """
    connect_client_name = "increment"
    _client = None

    def __init__(self):
#        self.key = self.__class__.get_kvs_key()
        self.init_value = 1 #settings.SERVERID * INIT_VALUE + 1

    @property
    def connect_client(self):            
        if not hasattr(self, "_client") or not self._client:
            config = settings.REDIS_CACHES[self.connect_client_name]
            self._client =self.__class__.get_client(config)
        return self._client 

    def incr(self, name):
        key = self.__class__.get_kvs_key(name)
        value = self.connect_client.incrby(key, INCREMENT)
        if value < self.init_value:
            value = self.init_value
            self.connect_client.set(key, value)
        return long(value)
 
    def get(self, name):
        key = self.__class__.get_kvs_key(name)
        value = self.connect_client.get(key, name)
        return self.init_value if value is None else long(value)

_IncrementId_instance = IncrmentId()
