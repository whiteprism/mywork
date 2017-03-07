# -*- coding: utf-8 -*-
from mongoengine import *
from common.docs import PlayerRedisDataBase
import datetime
from arenashop.api import get_arenashops
import random
from utils import random_items_pick, datetime_to_unixtime

class PlayerArenaShop(PlayerRedisDataBase):
    """
    用户荣誉商店信息
    """
    buyItem = ListField(default=[]) #已经购买item
    shopItem = ListField(default=[]) #可以购买item
    autoRefreshAt = DateTimeField(default=datetime.datetime.now)
    #refreshTimes = IntField(default=0) #每天刷新次数
    REFRESH_HOURS = [23, 11, 0]

    def new(self, player):
        super(self.__class__, self).new(player)
        self.refresh()

    def load(self, player):
        super(self.__class__, self).load(player)
        self.refresh_auto()

        now = datetime.datetime.now()
        if now.date() < self.updated_at.date():
            self.refreshTimes = 0
            self.update()
    '''
    def refresh_auto(self):
        now = datetime.datetime.now()
        if self.autoRefreshAt.date() == now.date():
            return False

        self.autoRefreshAt = now
        self.refresh()
        return True
    '''

    @classmethod
    def _before_refresh_hour(cls, hour):
        for _h in cls.REFRESH_HOURS:
            if _h < hour:
                return _h
        return _h

    @classmethod
    def _next_refesh_hour(cls, hour):
        before_hour = cls._before_refresh_hour(hour)
        _index = cls.REFRESH_HOURS.index(before_hour)
        return cls.REFRESH_HOURS[_index-1]

    @property
    def leftRefreshTime(self):
        """
        剩余自动刷新时间
        """
        now = datetime.datetime.now()
        next_refesh_hour = PlayerArenaShop._next_refesh_hour(now.hour)
        end_time = datetime.datetime(now.year, now.month, now.day, next_refesh_hour, 59, 59) + datetime.timedelta(seconds=4)
        #return ( end_time - now ).total_seconds() + 4
        return datetime_to_unixtime(end_time)

    def refresh_auto(self):
        now = datetime.datetime.now()
        if self.autoRefreshAt.date() == now.date():

            if PlayerArenaShop._before_refresh_hour(self.autoRefreshAt.hour)  ==  PlayerArenaShop._before_refresh_hour(now.hour) :
                return False
        #else:
            #0点更新
            #self.refreshCount = 0
            #self.diamondRefreshCount = 0
        self.autoRefreshAt = now
        self.refresh()
        return True

    '''
    def can_refresh_manual(self):
        return self.refreshTimes < 1

    @property
    def dailyRefreshLeftTimes(self):
        times = 1 - self.refreshTimes
        return times if times > 0 else 0

    def refresh_manual(self):
        self.refreshTimes += 1
        self.refresh()
        return True
    '''

    '''
    @property
    def leftRefreshTime(self):
        """
        剩余自动刷新时间
        """
        now = datetime.datetime.now()
        end_time = datetime.datetime(now.year, now.month, now.day, 0, 0, 3) +  datetime.timedelta(1)
        return ( end_time - now ).total_seconds()
    '''

    def refresh(self):
        self.buyItem = []
        _arenashops = get_arenashops()

        # 这里修改为取固定地方的物品，不采用随机概率的方式了，5.26
        type1 = []
        type2 = []
        type3 = []
        type4 = []

        arenashops = [(p, p.type) for p in _arenashops]
        for k, t in arenashops:
            if t == 1:
                type1.append(k.pk)
            elif t == 2:
                type2.append(k.pk)
            elif t == 3:
                type3.append(k.pk)
            elif t == 4:
                type4.append(k.pk)

        self.shopItem = []
        self.shopItem.extend(random.sample(type1, 8))
        self.shopItem.extend(random.sample(type2, 2))
        self.shopItem.extend(random.sample(type3, 4))
        self.shopItem.extend(random.sample(type4, 2))
        self.update()

    def can_exchange(self, shop_id):
        shop_id = int(shop_id)
        if shop_id not in self.shopItem:
            return False
        if shop_id in self.buyItem:
            return False

        return True

    def exchange(self, shop_id):
        shop_id = int(shop_id)
        self.buyItem.append(shop_id)
        self.update()

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["leftRefreshTime"] = self.leftRefreshTime
        #dicts["dailyRefreshLeftTimes"] = self.dailyRefreshLeftTimes
        del dicts["autoRefreshAt"]
        return dicts
