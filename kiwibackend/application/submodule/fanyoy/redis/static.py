# -*- coding: utf-8 -*-
#from .client import get_client
import hashlib
from django.conf import settings
import random
import time
from module.utils import unixtime_to_datetime
from base import *
try:
    import cPickle as pickle
except:
    import pickle

class StaticRedisHandler(RedisHandlerBase):
    """
    静态数据redis操作
    """
    _client = None
    _connect_client_name = DEFAULT_DB

    @classmethod
    def connect_client(cls):
        if not hasattr(cls, "_client") or not  cls._client:
            config = cls.get_connect_client_config()
            cls._client =cls.get_client(config)
        return cls._client

    @classmethod                               
    def get_connect_client_config(cls):
        configs = settings.REDIS_CACHES[cls._connect_client_name]
        class_hash = hashlib.md5(cls.__name__).hexdigest()[-6:]
        class_int = int(class_hash, 16) % len(configs)
        return  configs[class_int]

class StaticSingleDataRedisHandler(StaticRedisHandler):
    """
    静态数据
    单一数据操作
    """
    @classmethod
    def get(cls, key="ALL", default=""):
        value = cls.connect_client().get(cls.get_kvs_key(key))
        if value is None:
            value = default

        return value
            
    @classmethod
    def set(cls, value, key="ALL"):
        return cls.connect_client().set(cls.get_kvs_key(key), value)
    
    @classmethod
    def incrby(cls, delta_value, key="ALL"):
        """
        只有存储值为int时进行原子操作
        """
        try:
            delta_value = int(delta_value)
            value = cls.connect_client().incr(cls.get_kvs_key(key), delta_value)
            return value
        except:
            return 0

class StaticSetDataRedisHandler(StaticRedisHandler):
    """
    静态数据
    公用集合部分（非排序类）
    """

    @classmethod
    def get_all(cls, key="ALL"):
        """
        获得集合全部元素
        return []
        Return all members of the set name
        """
        return list(cls.connect_client().smembers(cls.get_kvs_key(key)))

    @classmethod
    def count(cls, key="ALL"):
        """
        获得长度
        return int
        Return the number of elements in set name
        """
        return cls.connect_client().scard(cls.get_kvs_key(key))

    @classmethod
    def exists(cls, value, key="ALL"):
        """
        检查是否存在value值
        return Boolean
        Return a boolean indicating if value is a member of set name
        """
        return cls.connect_client().sismember(cls.get_kvs_key(key), value)

    @classmethod
    def add(cls, value, key="ALL"):
        """
        集合中添加元素
        Add value(s) to set name
        """
        cls.connect_client().sadd(cls.get_kvs_key(key), value)
    
    @classmethod
    def remove(cls, values, key="ALL"):
        """
        删除元素
        Remove values from set name
        """
#         if type(values) != list:
#             values = [values] #list转化
        cls.connect_client().srem(cls.get_kvs_key(key), values)

    @classmethod
    def random(cls, count, key="ALL"):
        """
        随机获得一定数量members
        If number is None, returns a random member of set name.
        If number is supplied, returns a list of number random memebers of set name. Note this is only available when running Redis 2.6+.
        """
        if count == 1:
            return cls.connect_client().srandmember(cls.get_kvs_key(key))
        else:
            return cls.connect_client().srandmember(cls.get_kvs_key(key), count)
            

class StaticSortedSetDataRedisHandler(StaticRedisHandler):
    """
    静态数据
    公用集合部分（排序类）
    """

    @classmethod
    def length(cls, key="ALL"):
        """
        获得长度
        return int
        Return the number of elements in the sorted set name
        """
        return cls.connect_client().zcard(cls.get_kvs_key(key))

    @classmethod
    def range(cls,start, end, key="ALL", desc=True, withscores=True,score_cast_func=float):
        """
        获得排行榜范围
        if withscores:
            return [(),()]
        else:
            return []
        Return a range of values from sorted set name between start and end sorted in ascending order.
        start and end can be negative, indicating the end of the range.
        desc a boolean indicating whether to sort the results descendingly
        withscores indicates to return the scores along with the values. The return type is a list of (value, score) pairs
        score_cast_func a callable used to cast the score return value
        """
        if not desc:
            return cls.connect_client().zrange(cls.get_kvs_key(key), start, end, desc, withscores, score_cast_func)
        else:
            return cls.connect_client().zrevrange(cls.get_kvs_key(key), start, end, withscores, score_cast_func)

    @classmethod
    def rangebyscore(cls, min_score, max_score, key="ALL", start=None, num=None, withscores=True, desc=True, score_cast_fun=float):
        """
        根据积分范围获取数据
        if withscores:
            return [(),()]
        else:
            return []
        Return a range of values from the sorted set name with scores between min and max.
        If start and num are specified, then return a slice of the range.
        withscores indicates to return the scores along with the values. The return type is a list of (value, score) pairs
        score_cast_func` a callable used to cast the score return value
        """
        if desc:
            return cls.connect_client().zrevrangebyscore(cls.get_kvs_key(key), max_score, min_score, start, num, withscores, score_cast_fun)
        else:
            return cls.connect_client().zrangebyscore(cls.get_kvs_key(key), min_score, max_score, start, num, withscores, score_cast_fun)

    @classmethod
    def rank(cls, value, key="ALL", desc=True):
        """
        返回排名 0,1,2,3,4,5
        0 为没有名次, 其他为正式排名
        return int
        Returns a 0-based value indicating the rank of value in sorted set name
        """
        if desc :
            rank = cls.connect_client().zrevrank(cls.get_kvs_key(key), value)
        else:
            rank = cls.connect_client().zrank(cls.get_kvs_key(key), value)

        if rank == None:
            rank = 0 #没有名次的默认为0
        else:
            rank += 1 #0-base 从redis中取出来从0开始
        return rank

    @classmethod
    def score(cls, value, key="ALL", default=0, init_default=False):
        """
        返回有序集 key 中，成员 member 的 score 值。
        return float
        Return the score of element value in sorted set name
        """
        score = cls.connect_client().zscore(cls.get_kvs_key(key), value)
        if score == None:
            score = default
            if init_default:
                cls.add({value: default}, key=key)

        return score

    @classmethod
    def rankandscore(cls, value, key="ALL", default_value=0, desc=True):
        """
        返回排名和积分
        return int, float
        """
        pipeline = cls.connect_client().pipeline()
        if desc:
            pipeline.zrevrank(cls.get_kvs_key(key), value)
        else:
            pipeline.zrank(cls.get_kvs_key(key), value)
        pipeline.zscore(cls.get_kvs_key(key), value)
        rank, score = pipeline.execute()

        if rank == None:
            rank = 0 #没有名次的默认为0
        else:
            rank += 1 #0-base 从redis中取出来从0开始

        if score == None:
            score = default_value
        return rank,score

    @classmethod
    def incrby(cls, value, delta_score=1, key="ALL"):
        """
        积分增加,返回总积分
        return float
        Increment the score of value in sorted set name by delta_score
        """
        return  cls.connect_client().zincrby(cls.get_kvs_key(key), value, delta_score)

    @classmethod
    def add(cls, values_scores, key="ALL"):
        """
        集合中添加元素 可以被incrby替换
        传入字典类型 values_scores is dict
        """
        params = []
        for k, v in values_scores.items():
            params.append(k)
            params.append(v)

        cls.connect_client().zadd(cls.get_kvs_key(key), *params)
    
    @classmethod
    def remove(cls, values, key="ALL"):
        """
        删除values
        Remove member values from sorted set name
        """
        if type(values) != list:
            values = [values]
        cls.connect_client().zrem(cls.get_kvs_key(key), *values)
    
class StaticDataRedisHandler(StaticRedisHandler):
    """
    静态数据
    作为mysql数据的缓存层
    """

    _id_to_instance = None
    _expire_time = 600    # 600
    _CACHE_FKS = {}
    _expire_cache_at = 0
    @classmethod
    def is_expired(cls):
        now = int(time.time())
        if now - cls._expire_cache_at < cls._expire_time:
            return False
        return True
    @classmethod
    def set_expire(cls):
       cls._expire_cache_at = int(time.time())

    @classmethod
    def create_cache(cls): 
        cls.create_cache_all()
        cls.create_cache_by_foreignkey()

    @classmethod
    def create_cache_all(cls): 
        instance_list = list(cls.objects.all())
        id_to_instance = dict([(instance.pk, instance) for instance in instance_list])
        if settings.ENABLE_REDIS_CACHE:
            cls.redis_set(cls.get_kvs_key(), id_to_instance)
        cls._id_to_instance = id_to_instance
        cls.set_expire()

    @classmethod
    def create_cache_by_foreignkey(cls): 

        fks = cls._CACHE_FKS
        if not fks:
            return

        instance_list = list(cls.objects.all())
        _id_to_instance_foreignkey = dict([(fk, {}) for fk in fks])

        for instance in instance_list:
            for fk in fks:
                fk_value = str(getattr(instance, fk))
                if fk_value not in _id_to_instance_foreignkey[fk]:
                    _id_to_instance_foreignkey[fk][fk_value] = []
                _id_to_instance_foreignkey[fk][fk_value].append(instance)

        cls._id_to_instance_foreignkey = _id_to_instance_foreignkey
        #print _id_to_instance_foreignkey
        if settings.ENABLE_REDIS_CACHE:
            cls.redis_set(cls.get_kvs_key("FK"), _id_to_instance_foreignkey)

    @classmethod
    def redis_get(cls, kvs_key):
        """
        redis 获取数据
        """
        instances = cls.connect_client().get(kvs_key)
        if instances:
            datas = pickle.loads(instances)
            return datas
        return None
            
    @classmethod
    def redis_set(cls, kvs_key, instances): 
        """
        redis 设置数据
        """
        cls.connect_client().set(kvs_key, pickle.dumps(instances))

    @classmethod
    def get(cls, instance_id):
        """
        获取对象
        """
        if instance_id is None:
            return None
        try:
            instance_id = int(float(instance_id))
        except:
            instance_id = instance_id
    
        id_to_instance = None 

        if settings.ENABLE_REDIS_CACHE and cls.is_expired():
            cls.create_cache()

        if hasattr(cls, '_id_to_instance') and cls._id_to_instance:
            id_to_instance = cls._id_to_instance
        else:      
            #id_to_instance = cls.redis_get(cls.get_kvs_key())
            #if id_to_instance:
            #    cls._id_to_instance = id_to_instance

            #if id_to_instance is  None:
            cls.create_cache()
            id_to_instance = cls._id_to_instance if cls._id_to_instance else {}

        if instance_id in id_to_instance:
            return id_to_instance[instance_id]

        return None

    @classmethod
    def get_all_list(cls):
        return cls.get_all_dict().values()
        
    @classmethod
    def get_all_dict(cls):
        """
        获取全部对象 字典
        """
        if  settings.ENABLE_REDIS_CACHE and cls.is_expired():
            cls.create_cache()
        if hasattr(cls, '_id_to_instance') and cls._id_to_instance:
            id_to_instance = cls._id_to_instance
        else:      
            #id_to_instance = cls.redis_get(cls.get_kvs_key())

            #if id_to_instance:
            #    cls._id_to_instance = id_to_instance

            #if id_to_instance is None:
            cls.create_cache()
            id_to_instance = cls._id_to_instance if cls._id_to_instance else {}

        return id_to_instance

    @classmethod
    def get_list_by_foreignkey(cls, fk):
        """
        通过外键获取对象 字典
        """
        if settings.ENABLE_REDIS_CACHE and cls.is_expired():
            #print "%s foreignkey cache  is expire" % cls.__name__
            cls.create_cache()
        if hasattr(cls, '_id_to_instance_foreignkey') and cls._id_to_instance_foreignkey:
            #print "%s foreignkey cache  read from mem" % cls.__name__
            id_to_instance_foreignkey = cls._id_to_instance_foreignkey
        else:      
            #print "%s foreignkey cache  read from redis start" % cls.__name__
            #id_to_instance_foreignkey = cls.redis_get(cls.get_kvs_key("FK"))

            #if id_to_instance_foreignkey:
            #    cls._id_to_instance_foreignkey = id_to_instance_foreignkey

            #if id_to_instance_foreignkey is None:
            #print "%s foreignkey cache  read from redis error" % cls.__name__
            cls.create_cache_by_foreignkey()
            id_to_instance_foreignkey = cls._id_to_instance_foreignkey if cls._id_to_instance_foreignkey else {}

        if fk in id_to_instance_foreignkey:
            return id_to_instance_foreignkey[fk]
        return {}

class StaticListRedisHandler(StaticRedisHandler):
    """
    数组
    """
    
    @classmethod
    def add(cls, key="ALL", members=[]):
        """
        添加member
        """
        if type(members) != list:
            members = [members]
    
        self.__class__.connect_client().rpush(cls.get_kvs_key(key), *members)

    @classmethod
    def len(cls, key="ALL"):
        """
        长度
        """
        return self.__class__.connect_client().llen(cls.get_kvs_key(key))

    @classmethod
    def set(cls, index, member, key="ALL"):
        return self.__class__.connect_client().lset(cls.get_kvs_key(key), index, member)

    @classmethod
    def all(cls, key="ALL"):
        return list(self.__class__.connect_client().lrange(cls.get_kvs_key(key), 0, -1))
