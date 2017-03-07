# -*- coding: utf-8 -*-
from mongoengine import *
from common.docs import PlayerDataBase, PlayerRelationBase, PlayerRedisDataBase
import datetime
import random
from module.vip.api import get_vip
from mysteryshop.models import MysteryShop
from module.common.static import Static
from module.mysteryshop.api import get_mysteryshopgrids, get_mystershopitems_by_show_id

class PlayerMysteryShop(PlayerRedisDataBase):
    """
    用户神秘商店信息
    """
    buyItem = ListField(default=[]) #已经购买item
    #refreshCount = IntField(default=0) #免费今日刷新次数
    #diamondRefreshCount = IntField(default=0) #元宝今日刷新次数
    shopItem = ListField(default=[]) #可以购买item
    autoRefreshAt = DateTimeField(default=datetime.datetime.now)
    refreshAt = DateTimeField(default=datetime.datetime.now)
    REFRESH_HOURS = [23, 11, 0]

    def new(self,player):
        super(self.__class__, self).new(player)
        self.refresh()

    @property
    def free_number(self):
        vip = get_vip(self.player.vip_level)
        return vip.refreshMysteryShopCount

    @property
    def yuanbo_number(self):
        return 100

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
        next_refesh_hour = PlayerMysteryShop._next_refesh_hour(now.hour)
        end_time = datetime.datetime(now.year, now.month, now.day, next_refesh_hour, 59, 59)
        return ( end_time - now ).total_seconds() + 4

    def refresh_auto(self):
        now = datetime.datetime.now()
        if self.autoRefreshAt.date() == now.date():

            if PlayerMysteryShop._before_refresh_hour(self.autoRefreshAt.hour)  ==  PlayerMysteryShop._before_refresh_hour(now.hour) :
                return False
        #else:
            #0点更新
            #self.refreshCount = 0
            #self.diamondRefreshCount = 0
        self.autoRefreshAt = now
        self.refresh()
        return True

    # def init_free(self):
    #     now = datetime.datetime.now()
    #     if self.refreshAt.date() != now.date():
            #self.refreshCount = 0
            #self.diamondRefreshCount = 0
            #self.update()
        #     return True
        # return False

    # def refresh_free(self):
    #     now = datetime.datetime.now()
    #     if self.refreshAt.date() == now.date():
    #         if self.refreshCount >= self.free_number:
    #             return False
    #     else:
    #         self.refreshCount = 0
    #         self.diamondRefreshCount = 0

    #     self.refreshAt = now
    #     self.refreshCount += 1
    #     self.refresh()
    #     return True

    @property
    def refreshCostYuanbo(self):
        #costYuanbo = 0
        #now = datetime.datetime.now()

        #if self.refreshAt.date() != now.date():
        #    self.refreshCount = 0
        #    self.diamondRefreshCount = 0

        #if self.diamondRefreshCount < 3:
        #    costYuanbo = 2 ** self.diamondRefreshCount * Static.MYSTERYSHOP_REFRESH_YUANBO
        #else:
        #    costYuanbo = (self.diamondRefreshCount - 2) * 60 + 80
        return Static.MYSTERYSHOP_REFRESH_YUANBO
        #return costYuanbo


    def refresh_yuanbo(self):
        now = datetime.datetime.now()
        #使用钻石刷新次数不做限制
        #if self.diamondRefreshCount >= self.yuanbo_number:
            #return False

        self.refreshAt = now
        #self.diamondRefreshCount += 1
        self.refresh()
        return True

    def refresh_ticket(self):
        self.refresh()
        return True

    def _refresh(self):
        #count = 24
        # 刷新不分普通还是高级ｖｉｐ　统一显示最多
        self.shopItem = []
        self.buyItem = []
        grids = get_mysteryshopgrids()

        for grid in grids:
            showItems = []
            for category in grid.categories:
                showItems += get_mystershopitems_by_show_id(category)

            while True:
                _shopitem = random.choice(showItems)
                if _shopitem.pk not in self.shopItem:
                    self.shopItem.append(_shopitem.pk)
                    break

        # for show_id in show_ids:
        #     for _id in show_id:
        #         shopitems.append(MysteryShop.get_items_by_show_id(show_id))

        #     if not shopitems:
        #         break

        #     _shopitem = random.choice(shopitems)
        #     #for _shopitem in sample_shopitems:
        #     self.shopItem.append(_shopitem.pk)

        '''
        vip1_show_ids = MysteryShop.vip1_show_ids()
        for show_id, number in vip1_show_ids:
            shopitems = MysteryShop.get_items_by_show_id(show_id)

            if not shopitems:
                break

            sample_shopitems = random.sample(shopitems, number)

            for _shopitem in sample_shopitems:
                self.shopItem.append(_shopitem.pk)
        '''
        return True

    # def _refresh_vip12(self):
    #     vip2_show_ids = MysteryShop.vip2_show_ids()
    #     for show_id, number in vip2_show_ids:
    #         shopitems = MysteryShop.get_items_by_show_id(show_id)
    #
    #         if not shopitems:
    #             break
    #
    #         sample_shopitems = random.sample(shopitems, number)
    #
    #         for _shopitem in sample_shopitems:
    #             self.shopItem.append(_shopitem.pk)
    #
    #     self.update()
    #
    #     return True

    #def refresh_with_vip(self):
    #    result = True
        # if len(self.shopItem) == 16 and self.player.vip_level >= 10:
        #self._refresh_vip10()
        # result = True

    #     if len(self.shopItem) == 16 and self.player.vip_level >= 12:
    #         self._refresh_vip12()
    #         result = True

    #    return result

    def refresh(self):
        # self.buyItem = []
        # self.shopItem = []

        self._refresh()
        # if self.player.vip_level >= 10:
        #self._refresh_vip10()

        # if self.player.vip_level >= 12:
        #     self._refresh_vip12()

        self.update()
        return True

    def can_exchange(self, shop_id):
        shop_id = int(shop_id)
        if shop_id not in self.shopItem:
            return False

        if self.player.vip_level < 10:
            index = self.shopItem.index(shop_id)
            if index > 15:
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
        #refreshCount = self.free_number - self.refreshCount
        #dicts["refreshCount"] = self.refreshCount #和宝石商店表达意思正好相反，宝石商店和vip无关，传递还能刷几次。神秘商店和vip有关，传递刷了几次

        del dicts["autoRefreshAt"]
        del dicts["refreshAt"]
        return dicts
