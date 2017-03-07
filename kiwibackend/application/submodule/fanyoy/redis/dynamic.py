# -*- coding: utf-8 -*-
import md5
from django.conf import settings
import random
import time
from module.utils import unixtime_to_datetime
from .increment import _IncrementId_instance
from .base import *
import redis
import time
from .static import StaticRedisHandler

class DynamicRedisHandler(RedisHandlerBase):
    """
    动态数据存储
    """
    _client = {}
    _connect_client_name = DEFAULT_DYNAMIC_DB
    
    @classmethod
    def connect_client(cls, key):
        class_int = cls.get_client_config_int(key)
        if not hasattr(cls, "_client") or not  class_int in cls._client:
            config = settings.REDIS_CACHES[cls._connect_client_name][class_int] 
            client =cls.get_client(config)
            cls._client[class_int] = client
        return cls._client[class_int]

    @classmethod
    def get_client_config_int(cls, key):
        """
        获得配置
        """
        configs = settings.REDIS_CACHES[cls._connect_client_name]
        class_hash = md5.md5(str(key)).hexdigest()[-6:]
        class_int = int(class_hash, 16) % len(configs)
        return class_int

    @classmethod
    def get_client_config(cls, key):
        class_int = cls.get_client_config_int(key)
        return settings.REDIS_CACHES[cls._connect_client_name][class_int] 
        

    @classmethod
    def delete(cls, keys):
        if type(keys) != list:
            keys = [keys] 
        cls.connect_client().delete(keys)

    @classmethod
    def acquire_lock(cls, tag_id, expire=10):
        conn = cls.connect_client(tag_id)
        lockname = "%s:Lock" % cls.get_kvs_key(tag_id)
        print lockname

        if conn.setnx(lockname, cls.__name__):
            print 1111, expire
            conn.expire(lockname, expire)
            return True

        #if not conn.ttl(lockname):
        #    print 22222
        #    conn.expire(lockname, expire)

        time.sleep(0.1)#等待0.1s

        return False
    
    @classmethod
    def release_lock(cls, tag_id):
        pipe = cls.connect_client(tag_id).pipeline(True)
        lockname = "%s:Lock" % cls.get_kvs_key(tag_id)
        while True:
            try:
                pipe.watch(lockname)
                if pipe.get(lockname) == cls.__name__:
                    pipe.multi()
                    pipe.delete(lockname)
                    pipe.execute()
                    return True
                pipe.unwatch()
                break
            except redis.exceptions.WatchError:
                pass
 
        # we lost the lock
        return False


# class GameDynamicRedisHandler(StaticRedisHandler):
#     """
#     游戏动态数据
#     """
#     _save_data = {} #需要保存到数据库的
#     keys = ['gashapon_data']
# 
#     @classmethod
#     def get(cls, key):
#         """
#         获取用户数据
#         """
#         key = str(key)
#         instance = cls.connect_client().hget(key, key)
#         return instance
# 
#     @classmethod
#     def save(cls, key):
#         """
#         保存到redis里
#         """
#         key = str(key)
#         if key not in cls.keys:
#             raise HandlerError, "no this key" 
#         client = cls.connect_client() #redis 链接库 
#         client.hset(key, key, cls._save_data)
#         cls._save_data = {}
#         return True
#             
#     @classmethod
#     def delete(cls, key):
#         """
#         删除
#         """
#         key = str(key)
#         if key not in cls.keys:
#             raise HandlerError, "no this key" 
#         client = cls.connect_client() #redis 链接库 
#         client.delete(key)
#         cls._save_data = {}
#         return True
    
class GameDynamicRedisHandler(StaticRedisHandler):
    """
    游戏动态数据
    """
    _save_data = [] #需要保存到数据库的
    keys = []

    @classmethod
    def get_all(cls, key):
        key = str(key)
        if key not in cls.keys:
            raise HandlerError, "no this key" 
        if not cls._save_data:
            cls._save_data = list(cls.connect_client().lrange(key, 0, -1))
            return cls._save_data
        return cls._save_data
    
    @classmethod
    def add(cls, key, value):
        """
        向末尾添加
        """
        key = str(key)
        value = str(value)
        if key not in cls.keys:
            raise HandlerError, "no this key" 
        client = cls.connect_client() #redis 链接库 
        client.rpush(key, value)
        cls._save_data = []
        return True
            
    @classmethod
    def remove(cls, key):
        '''
        移除头元素
        '''
        key = str(key)
        if key not in cls.keys:
            raise HandlerError, "no this key" 
        client = cls.connect_client() #redis 链接库 
        client.lpop(key)
        if cls._save_data:
            del cls._save_data[0]
        return True

class PlayerDynamicRedisHandler(DynamicRedisHandler):
    """
    用户系统 or 一对一关系
    """
    _all_params = {
        "id" : {
            'default': 0,  'type': int,
        }, 
        "_updated_at": { 
            'default': 0,  'type': int,
        }, #更新时间
        "_created_at": {
            'default': 0,  'type': int,
        }, #保存时间
    } #默认参数

    all_params = {} #各个对象自定义参数
    _save_data = {} #需要保存到数据库的
    _be_deleted = False #标志删除

    @classmethod
    def _params(cls):
        """
        所有参数
        """
        all_params = cls.all_params
        all_params.update(cls._all_params)
        return all_params

    def __init__(self, datas):
        """
        初始化对象
        """
        self._save_data = {}
        self._be_deleted = False
        all_params = self.__class__._params()
        for name,value in all_params.items():
            _value = datas.get(name)
            if not _value:
                _value = value['default']
            else:
                _value = value['type'](_value)

            setattr(self, name, _value)

    def __getattribute__(self, name):  
        if object.__getattribute__(self, "_be_deleted") == True:
            raise AttributeError, "object is be deleted, can not be gotten again"
        return object.__getattribute__(self, name)  

    def __getattr__(self, name):
        raise AttributeError, "the object %s attr %s does not exist" % (self.__class__.__name__, name)


    def set(self, name, value):
        """
        保存数据
        """
        #安全检查
        if name not in self.__class__._params():
            return False 

        value = self.__class__._params()[name]["type"](value)
        if not hasattr(self, name) or getattr(self, name) != value:
            setattr(self, name, value)
            self._save_data[name] = value
    
    @classmethod
    def get(cls, tag_id, keys=[]):
        """
        获取用户数据
        """
        tag_id = int(tag_id)
        if keys:
            keys.append("id")
            keys.append("_updated_at")
            keys.append("_created_at")
            instance = cls.connect_client(tag_id).hmget(cls.get_kvs_key(tag_id), keys)
            instance = dict(zip(keys, instance))
        else:
            instance = cls.connect_client(tag_id).hgetall(cls.get_kvs_key(tag_id))

        if instance:
            return cls(instance)
        return None

    @classmethod
    def exists(cls, tag_id):
        """
        探测用户是否在redis中
        """
        tag_id = int(tag_id)
        return cls.connect_client(tag_id).exists(cls.get_kvs_key(tag_id))

    @classmethod
    def create(cls, *args, **kwargs):
        """
        创建数据
        """
        #　传入的参数一定要包含ｉｄ信息
        if "id" not in kwargs:
            raise HandlerError, "id is not in redis"
        kwargs["id"] = int(kwargs.get("id"))
        if cls.exists(kwargs["id"]):
            raise HandlerError, "id is already in redis" 
        params = cls._params()
        #　类自身所带的各种以XXX_bin结尾的参数，和创建时传入的参数去做交集，得到一个结果.
        common_keys = set(params.keys()).intersection(set(kwargs.keys()))
        create_datas = {}
        # 我个人理解这里只有一个共同的id,字段，当没有取到数据时.
        for common_key in common_keys:
            create_datas[common_key] =  params[common_key]["type"](kwargs[common_key])
        create_datas["_updated_at"] = int(time.time()) #更新时间
        create_datas["_created_at"] = int(time.time()) #更新时间
        # 创建相应的字段信息的数据.
        client = cls.connect_client(create_datas["id"]) #redis 链接库
        pipeline = client.pipeline() #pipline
        pipeline.hmset(cls.get_kvs_key(create_datas["id"]), create_datas) #hash存储
        pipeline.hgetall(cls.get_kvs_key(create_datas["id"]))#获取插入数据
        result = pipeline.execute() #执行 [True, instance, True]
        return cls(result[1])

    def save(self):
        """
        保存到redis里
        """
        if not self._be_deleted:
            self._save_data["_updated_at"] = int(time.time()) #更新时间
            client = self.__class__.connect_client(self.id) #redis 链接库 
            client.hmset(self.__class__.get_kvs_key(self.id),self._save_data)
            self._save_data = {}
        return True
            
    def delete(self):
        """
        删除
        """
        client = self.__class__.connect_client(self.id) #redis 链接库 
        client.delete(self.__class__.get_kvs_key(self.id))
        self._be_deleted = True
        self._save_data = {}
        return True

    @property
    def updated_at(self):
        return unixtime_to_datetime(self._updated_at)    
    @property
    def created_at(self):
        return unixtime_to_datetime(self._created_at)


class PlayerDynamicObjectsRedisHandler(DynamicRedisHandler):
    """
    用户数据redis操作
    """
    _player_objects = {}
    _all_params = {
        "id" : {
            'default': 0,  'type': int,
        }, #自增ID,
        "player_id": {
            'default': 0,  'type': int,
        }, #用户ID
        "_updated_at": { 
            'default': 0,  'type': int,
        }, #更新时间
        "_created_at": {
            'default': 0,  'type': int,
        }, #保存时间
    } #默认参数

    all_params = {} #各个对象自定义参数
    _save_data = {} #需要保存到数据库的
    _be_deleted = False #标志删除
    save_by_target_player = False #根据target player 分别存储信息

    @classmethod
    def _params(cls):
        """
        所有参数
        """
        all_params = cls.all_params
        all_params.update(cls._all_params)
        return all_params

    def __init__(self, datas):
        """
        初始化对象
        """
        self._save_data = {}
        all_params = self.__class__._params()
        for name,value in all_params.items():
            setattr(self, name, value['type'](datas.get(name, value['default'])))

    def __getattribute__(self, name):  
        if object.__getattribute__(self, "_be_deleted") == True:
            raise AttributeError
        return object.__getattribute__(self, name)  

    def __getattr__(self, name):
            raise AttributeError, "the object %s attr %s does not exist" % (self.__class__.__name__, name)

    def set(self, name, value):
        """
        保存数据
        """
        all_params = self.__class__._params()
        #安全检查
        if name not in all_params:
            return False 

        value = all_params[name]["type"](value)
        if not hasattr(self, name) or getattr(self, name) != value:
            setattr(self, name, value)
            self._save_data[name] = value

    @classmethod
    def get_kvs_key_by_player(cls, player_id, key="ALL"):
        """
        获取KVS key
        """
        #print "%s:%s:%s:%s" % (settings.KVS_BASE_NAME, cls.__name__, player_id, key)
        return "%s:%s:%s:%s" % (settings.KVS_BASE_NAME, cls.__name__, player_id, key)

    @classmethod
    def _incrment_id(cls):
        """
        获取自增id
        """
        return _IncrementId_instance.incr(cls.__name__)
    
    @classmethod
    def get(cls, player_id, player_instance_id):
        """
        获取用户数据
        """
        player_id = int(player_id)
        player_instance_id = int(player_instance_id)
        instance = cls.connect_client(player_id).hgetall(cls.get_kvs_key(player_instance_id))
        if instance:
            return cls(instance)
        return None

    @classmethod
    def create(cls, *args, **kwargs):
        """       
        创建数据 
        """       
        player_id = int(kwargs.get("player_id", 0)) #获取用户id， create时必须要有自增player_id
        if not player_id:
            raise HandlerError, "when create player object, player_id must exist" 
         
        player_instance_id = int(cls._incrment_id()) #自增ID
        if cls.save_by_target_player:
            target_player_id = int(kwargs.get("target_player_id", 0))
            if not target_player_id:
                raise HandlerError, "when save_by_target_player is True, target_playerid must exist" 
        else :
            target_player_id = None
                  
        params = cls._params()
        common_keys = set(params.keys()).intersection(set(kwargs.keys()))
        create_datas = {}
        for common_key in common_keys:
            create_datas[common_key] =  params[common_key]["type"](kwargs[common_key])
        create_datas["_updated_at"] = int(time.time()) #更新时间
        create_datas["_created_at"] = int(time.time()) #更新时间
        create_datas["id"] = player_instance_id #加入自增ID

        client = cls.connect_client(player_id) #redis 链接库
        pipeline = client.pipeline() #pipline
        pipeline.hmset(cls.get_kvs_key(player_instance_id), create_datas) #hash存储
        pipeline.hgetall(cls.get_kvs_key(player_instance_id))#获取插入数据
        if target_player_id:
            pipeline.zadd(cls.get_kvs_key_by_player(player_id, target_player_id),  player_instance_id, int(time.time())) #插入用户list中
        else:
            pipeline.zadd(cls.get_kvs_key_by_player(player_id),  player_instance_id, int(time.time())) #插入用户list中
        result = pipeline.execute() #执行 [True, instance, True]
        cls._delete_memory_datas(player_id, target_player_id)
        return cls(result[1])
    
    @classmethod
    def _set_memory_datas(cls, player_id, datas, target_player_id=None):
        """
        获取内存中的数据
        """
        player_id = int(player_id)
        if target_player_id:
            #if player_id not in cls._player_objects or not cls._player_objects[player_id]:
            #    cls._player_objects[player_id] = {}
            #cls._player_objects[player_id][target_player_id]= datas
            key = '%s:%d:%d' % (cls.__name__, player_id, int(target_player_id))
            cls._player_objects[key]= datas
        else:
            cls._player_objects[player_id] = datas
    
    @classmethod
    def _get_memory_datas(cls, player_id, target_player_id=None):
        """
        获取内存中的数据
        """
        player_id = int(player_id)
        if target_player_id:
            key = '%s:%d:%d' % (cls.__name__, player_id, int(target_player_id))
            if key in cls._player_objects:
                return cls._player_objects[key]
            else:
                return []
        else:
            if player_id in cls._player_objects:
                return cls._player_objects[player_id]
        return []
        
    @classmethod
    def _delete_memory_datas(cls, player_id, target_player_id=None):
        """
        清空内存中的数据
        """
        player_id = int(player_id)
        #从内存中删除
        if player_id in cls._player_objects:
            if target_player_id:
                key = '%s:%d:%d' % (cls.__name__, player_id, int(target_player_id))
                if key in cls._player_objects:
                    del cls._player_objects[key]
            else:
                del cls._player_objects[player_id]

    @classmethod
    def get_all(cls, player_id, target_player_id=None):
        """
        获得用户
        """
        
        if cls.save_by_target_player and target_player_id:
            target_player_id = int(target_player_id)
            if not target_player_id:
                raise HandlerError, "when save_by_target_player is True, target_playerid must exist" 
        else :
            target_player_id = None
        
        player_id = int(player_id)
        #player_objects = cls._get_memory_datas(player_id, target_player_id)
        #if player_objects:
        #    return player_objects
        player_objects = []
        all_instances = []
        client = cls.connect_client(player_id) #redis 链接库
        if  target_player_id:
            player_instance_ids = client.zrange(cls.get_kvs_key_by_player(player_id, target_player_id), 0, -1, True) #倒序
        else:
            player_instance_ids = client.zrange(cls.get_kvs_key_by_player(player_id), 0, -1, True) #倒序
        if player_instance_ids:
            pipeline = client.pipeline() #pipline 
            for player_instance_id in player_instance_ids:
                pipeline.hgetall(cls.get_kvs_key(player_instance_id))
            all_instances = pipeline.execute()
            for instance in all_instances:
                player_objects.append(cls(instance))
            cls._set_memory_datas(player_id, player_objects, target_player_id)
        return player_objects

    def save(self):
        """
        保存到redis里
        """
        if self._save_data and not self._be_deleted:
            self._save_data["_updated_at"] = int(time.time()) #更新时间
            client = self.__class__.connect_client(self.player_id) #redis 链接库 
            client.hmset(self.__class__.get_kvs_key(self.id),self._save_data)
            self._save_data = {}
            if self.__class__.save_by_target_player:
                self.__class__._delete_memory_datas(self.player_id, self.target_player_id)
            else:
                self.__class__._delete_memory_datas(self.player_id)
        return True
    
    @classmethod
    def delete_all(cls, player_id, target_player_id=None):
        """
        删除全部
        """
        if not cls.save_by_target_player:
            target_player_id = None
            
        client = cls.connect_client(player_id) #redis 链接库 
        pipeline = client.pipeline()
        
        player_instances = cls.get_all(player_id, target_player_id)
        for player_instance in player_instances:
            pipeline.delete(cls.get_kvs_key(player_instance.id))
            
        if target_player_id:
            pipeline.delete(cls.get_kvs_key(player_id,target_player_id))
        else:
            pipeline.delete(cls.get_kvs_key(player_id))
            
        pipeline.execute()
        
        if target_player_id:
            cls._delete_memory_datas(player_id, target_player_id)
        else:
            cls._delete_memory_datas(player_id)
            
        #cls._be_deleted = True
        return True
    
    def delete(self):
        """
        删除
        """
        
        if self.__class__.save_by_target_player:
            target_player_id = self.target_player_id
        else:
            target_player_id = None
            
        client = self.__class__.connect_client(self.player_id) #redis 链接库 
        pipeline = client.pipeline()
        
        if target_player_id:
            pipeline.zrem(self.__class__.get_kvs_key_by_player(self.player_id, target_player_id), self.id)
        else:
            pipeline.zrem(self.__class__.get_kvs_key_by_player(self.player_id), self.id)
        pipeline.delete(self.__class__.get_kvs_key(self.id))
        pipeline.execute()
        
        if target_player_id:
            self.__class__._delete_memory_datas(self.player_id, self.target_player_id)
        else:
            self.__class__._delete_memory_datas(self.player_id)
            
        self._be_deleted = True
        return True
    
    @property
    def updated_at(self):
        return unixtime_to_datetime(self._updated_at)	
    @property
    def created_at(self):
        return unixtime_to_datetime(self._created_at)	

class PlayerDynamicSetRedisHandler(DynamicRedisHandler):
    """
    player 数据集合
    """
    
    _members= []

    def __init__(self, key=None, player_id=None):
        """
        redis 集合 存储
        """
        self.key = self.__class__.get_kvs_key(key)
        if not player_id:
            self.player_id = key
        self._members = list(self.__class__.connect_client(self.player_id).smembers(self.key))
        
    def add(self, members):
        """
        添加member
        """
        if type(members) != list:
            members = [members]
    
        for member in members:
            if member in self._members:
                continue
            self._members.append(member)
        
        self.__class__.connect_client(self.player_id).sadd(self.key, *members)

    def remove(self, members):

        if type(members) != list:
            members = [members]

        for member in members:
            if member in self._members:
                self._members.remove(member)
        self.__class__.connect_client(self.player_id).srem(self.key, *members)

    def get_all(self):
        return self._members

    def exists(self, member):
        return member in self._members
    
class PlayerDynamicListRedisHandler(DynamicRedisHandler):
    """
    player 数组
    """
    
    _members= []

    def __init__(self, key=None, player_id=None):
        """
        redis 数组 存储
        """
        self.key = self.__class__.get_kvs_key(key)
        if not player_id:
            self.player_id = key
            
        self._members = list(self.__class__.connect_client(self.player_id).lrange(self.key, 0, -1))
        
    def add(self, members):
        """
        添加member
        """
        if type(members) != list:
            members = [members]
    
        for member in members:
            if member in self._members:
                continue
            self._members.append(member)
        self.__class__.connect_client(self.player_id).rpush(self.key, *members)

    def remove(self, member, num=0):
        if member in self._members:
            self._members.remove(member)
            self.__class__.connect_client(self.player_id).lrem(self.key, member, num)
        
    def reset(self, index, member):
        self._members[index] = member
        self.__class__.connect_client(self.player_id).lset(self.key, index, member)

    def get_all(self):
        return self._members

    def exists(self, member):
        return member in self._members
    
class PlayerDynamicHashRedisHandler(DynamicRedisHandler):
    '''
    player 字典
    '''
    _members = {}
    
    def __init__(self, key=None, player_id=None):
        """
        redis 哈希 存储
        """
        self.key = self.__class__.get_kvs_key(key)
        if not player_id:
            self.player_id = key
            
        self._members = self.__class__.connect_client(self.player_id).hgetall(self.key)
        
    def add(self, key, value):
        self._members[key] = value
        self.__class__.connect_client(self.player_id).hset(self.key, key, value)
        
    def remove(self, key):
        del self._members[key]
        self.__class__.connect_client(self.player_id).hdel(self.key, key)
        
    def get_all(self):
        return self._members
    
    def get(self, key):
        return self._members[key]
    
    def exists(self, key):
        return self.__class__.connect_client(self.player_id).hexists(self.key, key)
    
        
