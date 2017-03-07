# -*- coding: utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler
from module.common.static import Static
from common.decorators.memoized_property import memoized_property
from module.rewards.api import get_commonreward

class MysteryShop(models.Model, StaticDataRedisHandler, CommonStaticModels):
    _CACHE_FKS = ["show_id"]
    SHEET_NAME = u"神秘商店"
    name = models.CharField(u"名字", max_length=50)
    rewardId = models.CharField(u"奖励Id",max_length=50,default="")
    gold = models.IntegerField(u"消耗荣誉点",default=0)
    diamond = models.IntegerField(u"消耗消耗",default=0)
    show_id = models.IntegerField(u"排序",default=0) #1-5普通 6-9 普通vip  10-13 超级vip
    vipLevelLimit = models.IntegerField(u"VIP等级限制",default=0)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()

        dicts["gid"] = dicts["id"]
        del dicts["id"]
        del dicts["name"]
        del dicts["show_id"]

        return dicts

    @memoized_property
    def reward(self):
        '''
        获得奖励
        '''
        return get_commonreward(self.rewardId)


    # def get_mysteryshopgrid(pk):
    #     return MysteryShopGrid.get(int(pk))

    # @classmethod
    # def get_show_ids():
    #     _show_ids = []
    #     maxLen = len(MysteryShopGrid.get_all_list())
    #     for _id in range(0, maxLen):
    #         _grid = get_mysteryshopgrid(_id)
    #         _category = _grid.categories_int
    #         _show_id = [category_single for category_single in _category.strip().split(",") if category_single]
    #         _show_ids.append(_show_id)
    #     return _show_ids

    '''
    @property
    def is_equipfragment(self):
        return self.category == 23

    @property
    def is_item(self):
        return self.category == 26

    @property
    def is_soul(self):
        return self.category == 20

    @property
    def is_artifactfragment(self):
        return self.category == 24s

    @classmethod
    def normal_show_ids(cls):
        return [(1, 2), (2,2), (3,2), (4,1), (5, 1), (11, 1), (12, 3), (13, 2), (14, 1), (15, 1)]


    @classmethod
    def vip1_show_ids(cls):
        return [(21, 4),(22, 2),(23, 2)]
    '''

    # @classmethod
    # def vip2_show_ids(cls):
    #     return [(21, 4),(22,2),(23,1),(24,1)]

    @classmethod
    def get_items_by_show_id(cls, show_id):
        _cache_data = cls.get_list_by_foreignkey("show_id")
        return _cache_data[str(show_id)] if str(show_id) in _cache_data else []

class MysteryShopGrid(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"神秘商店格子定义"
    categories_int = models.CharField(u"奖励Id",max_length=50,default="")


    @memoized_property
    def categories(self):
        if self.categories_int.strip():
            return [int(float(category)) for category in self.categories_int.strip().split(",") if category]
        return []
