# -*- encoding:utf8 -*-
from mongoengine import *
import datetime
from submodule.fanyoy.redis.increment import _IncrementId_instance
from common.decorators.memoized_property import memoized_property
from submodule.fanyoy.redis.dynamic import DynamicRedisHandler

class PlayerBase(Document, DynamicRedisHandler):
    """
    用户基础Cls
    """
    id = LongField(primary_key = True) 
    created_at = DateTimeField(default = datetime.datetime.now)  #作成日時
    updated_at = DateTimeField(default = datetime.datetime.now)
    meta = {
        'abstract': True,
    }
    def to_dict(self, keys=[]):
        if not keys:
            keys = self.__class__._fields.keys()
        dicts = {}

        for name in keys:
            dicts[name] = getattr(self, name)

        if "created_at" in dicts:
            del dicts["created_at"]

        if "updated_at" in dicts:
            del dicts["updated_at"]

        return dicts

    def save(self, *args, **kwargs):
        if not self.pk:
            self.pk = _IncrementId_instance.incr(self.__class__.__name__)
        self.updated_at = datetime.datetime.now()
        super(PlayerBase, self).save(*args, **kwargs)

class PlayerModifyBase(PlayerBase):
    """
    用户数据基础Cls
    """
    mKeys = [] #此次变动keys
    meta = {
        'abstract': True,
    }

    def __init__(self, *args, **kwargs):
        super(PlayerModifyBase, self).__init__(*args, **kwargs)
        self.mKeys = []

    def __setattr__(self, name, value):
        """
        赋值
        """
        keys = self.__class__._fields.keys()
        if (name in keys) and name not in ["updated_at", "created_at"]:
            self.set_modify(name)

        return super(PlayerModifyBase, self).__setattr__(name, value)

    def set_modify(self, name):
        if name not in self.mKeys:
            self.mKeys.append(name)

    @property
    def is_modify(self):
        return len(self.mKeys) > 0

    def to_dict(self, is_all=False):
        dicts = {}
        if not is_all and not self.mKeys:
            dicts["mKeys"] = ["_"]
            return dicts
        
        if is_all:
            dicts = super(PlayerModifyBase, self).to_dict()
        else:
            dicts = super(PlayerModifyBase, self).to_dict(self.mKeys)

        if is_all:
            dicts["mKeys"] = []
        else:
            dicts["mKeys"] = self.mKeys
        
        return dicts

class PlayerRelationBase(PlayerBase):
    """
    以用户ID作为主键
    """
    meta = {
        'abstract': True,
    }
#    @memoized_property
#    def player(self):
#        from module.player.api import get_player
#        return get_player(self.pk)


class PlayerDataBase(PlayerBase):
    """
    用户数据基础Cls
    """

    player_id = LongField()  #玩家id
   
    meta = {
        'abstract': True,
        "indexes":["player_id"],
    }

    #@memoized_property
    #def player(self):
    #    from module.player.api import get_player
    #    return get_player(self.player_id)
    

    
class PlayerRedisDataBase(PlayerBase):
    """
    用户数据基础Cls
    """
    meta = {
        'abstract': True,
    }

    def new(self, player):
        self.player = player

    def load(self, player):
        self.player = player

    def update(self):
        self.data_handler.update()

    @property
    def bin_data(self):
        return self.data_handler.bin_data

    def save(self):
        raise

class PlayerRedisDataModifyBase(PlayerRedisDataBase):
    """
    用户数据基础Cls
    """
    mKeys = [] #此次变动keys
    meta = {
        'abstract': True,
    }

    def new(self, player):
        super(PlayerRedisDataModifyBase, self).new(player)
        self.mKeys = []

    def load(self, player):
        super(PlayerRedisDataModifyBase, self).load(player)
        self.mKeys = []

    def __setattr__(self, name, value):
        """
        赋值
        """
        keys = self.__class__._fields.keys()

        if (name in keys) and name not in ["updated_at", "created_at"]:
            self.set_modify(name)

        return super(PlayerRedisDataModifyBase, self).__setattr__(name, value)

    def set_modify(self, name):
        if name not in self.mKeys:
            self.mKeys.append(name)

    @property
    def is_modify(self):
        return len(self.mKeys) > 0

    def to_dict(self, is_all=True):
        dicts = {}
        if not is_all and not self.mKeys:
            dicts["mKeys"] = ["_"]
            return dicts

        if is_all:
            dicts = super(PlayerRedisDataModifyBase, self).to_dict()
        else:
            dicts = super(PlayerRedisDataModifyBase, self).to_dict(self.mKeys)

        if is_all:
            dicts["mKeys"] = []
        else:
            dicts["mKeys"] = self.mKeys
        
        return dicts


class PlayerRedisDataListBase(PlayerRedisDataBase):
    """
    用户数据基础Cls
    数据结构
    id  data_id, count
    """
    meta = {
        'abstract': True,
    }
    obj_id = IntField() #前端的gid
    count = IntField(default=0) #数量

    def load(self, player):
        self.player = player

    def to_dict(self):
        dicts = super(PlayerRedisDataListBase, self).to_dict()
        del dicts["obj_id"]
        return dicts

    def can_sub(self, number=1):
        return self.count >= number
    
    @property
    def display(self):
        return self.count > 0

    def save(self):
        raise
