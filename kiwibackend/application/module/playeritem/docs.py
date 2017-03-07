# -*- coding: utf-8 -*-
from mongoengine import *
from common.docs import PlayerRedisDataListBase, PlayerRedisDataBase
from common.decorators.memoized_property import memoized_property
from module.item.api import get_item
import datetime
from common.actionlog import ActionLogWriter

class PlayerItem(PlayerRedisDataListBase):
    """
    用户物品
    """
    def __unicode__(self):
        return u"%s:%s(%s)" %(self.id, self.item_id, self.count)

    @memoized_property
    def item(self):
        return get_item(self.item_id)

    @property
    def item_id(self):
        return self.obj_id
    
    def sub(self, number=1, info=u""):
        before_number = self.count
        self.count -= number
        after_number = self.count
        ActionLogWriter.item_cost(self.player, self.item_id, before_number, after_number, info)
        if self.display:
            self.player.update_item(self, True)
        else:
            self.player.delete_item(self.pk, True)
            
        return True

    def add(self, delta_number=1, info=u""):
        before_number = self.count 
        self.count += delta_number
        after_number = self.count 
        ActionLogWriter.item_acquire(self.player, self.item_id, before_number, after_number, info)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["itemId"] = self.item_id
        return dicts

class PlayerStoreRecord(PlayerRedisDataListBase):
    """
    购买记录
    """
    item_id = IntField() #前端的gid
    dailyCount = IntField(default=0) 
    totalCount = IntField(default=0) 

    def buy(self, player, number, info=""):
        """
        购买次数
        """
        before_number = self.today_buy_number  
        self.dailyCount = self.today_buy_number + number
        after_number = self.today_buy_number  
        self.totalCount += number
        ActionLogWriter.item_buyrecord(player, self.item_id, before_number, after_number, self.totalCount, info)
        
    @property
    def today_buy_number(self):
        if not self.updated_at:
            return 0

        if self.updated_at.date() == datetime.datetime.now().date():
            return self.dailyCount
        else:
            return 0

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["dailyCount"] = self.today_buy_number
        dicts["itemId"] = self.item_id
        del dicts["item_id"]
        return dicts

class PlayerTowerStoreRecord(PlayerRedisDataListBase):
    """
    购买记录
    """
    item_id = IntField() #前端的gid
    dailyCount = IntField(default=0)
    totalCount = IntField(default=0)

    def buy(self, player, number, info=""):
        """
        购买次数
        """
        before_number = self.today_buy_number
        self.dailyCount = self.today_buy_number + number
        after_number = self.today_buy_number
        self.totalCount += number
        ActionLogWriter.item_buytowerrecord(player, self.item_id, before_number, after_number, self.totalCount, info)

    @property
    def today_buy_number(self):
        if not self.updated_at:
            return 0

        if self.updated_at.date() == datetime.datetime.now().date():
            return self.dailyCount
        else:
            return 0

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["dailyCount"] = self.today_buy_number
        dicts["itemId"] = self.item_id
        del dicts["item_id"]
        return dicts

