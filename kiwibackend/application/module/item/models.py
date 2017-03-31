# -*- coding: utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler
from common.decorators.memoized_property import memoized_property
from utils import datetime_to_unixtime,random_item_pick
from module.common.static import Static
import random


class Item(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"物品"
    name = models.CharField(u"name", max_length=200, default=0)
    boxId = models.IntegerField(u"宝箱id", default=0)
    boxKeyId = models.IntegerField(u"宝箱钥匙", default=0)
    gashapon_id = models.IntegerField(u"抽奖ID", default=0)
    canUse = models.BooleanField(u"是否可以使用", default=False)
    description = models.CharField(u"desc", max_length=200, default=0)
    descriptionId = models.CharField(u"desc id", max_length=200, default="")
    rewardIds_str = models.CharField(u"奖励", max_length=200, default="")
    icon = models.CharField(u"icon", max_length=200, default="")
    nameId = models.CharField(u"nameId", max_length=200, default="")
    quality = models.IntegerField(u"quality", default=0)
    orderId = models.IntegerField(u"orderId", default=0)
    category = models.IntegerField(u"type", default=0)
    searchDifficuty_int = models.CharField(u"出处所在关卡的难度", max_length=200, default="")
    searchInstances_int = models.CharField(u"出处所在关卡id", max_length=200, default="")
    number = models.IntegerField(u"数量", default=0)
    isChapter = models.IntegerField(u"章节判断", default=0)

    @property
    def is_power(self):
        """体力"""
        return self.category == Static.ITEM_TYPE_POWER

    @property
    def is_stamina(self):
        """耐力"""
        return self.category == Static.ITEM_TYPE_SP

    @property
    def is_gold(self):
        """金币"""
        return self.category == Static.ITEM_TYPE_GOLD

    @property
    def is_wood(self):
        """木头"""
        return self.category == Static.ITEM_TYPE_WOOD

    @property
    def is_refresh_ticket(self):
        """刷新券"""
        return self.category == Static.ITEM_TYPE_REFRESH_TICKET

    @property
    def is_sweep(self):
        """扫荡"""
        return self.category == Static.ITEM_TYPE_SWEEP

    @property
    def is_key(self):
        """钥匙"""
        return self.category == Static.ITEM_TYPE_KEY

    @property
    def is_box(self):
        """宝箱"""
        return self.category == Static.ITEM_TYPE_BOX

    @property
    def is_sliver_box(self):
        """银箱子"""
        return self.pk == Static.ITEM_SLIVER_BOX_ID

    @property
    def is_gold_box(self):
        """金箱子"""
        return self.pk == Static.ITEM_GOLD_BOX_ID

    @property
    def is_xp(self):
        """经验"""
        return self.category == Static.ITEM_TYPE_XP

    # @property
    # def is_waravoid(self):
    #     """免战牌"""
    #     return self.category == Static.ITEM_TYPE_WARAVOID

    @property
    def is_goldhand(self):
        """点金手"""
        return self.category == Static.ITEM_TYPE_GOLDHAND

    @property
    def is_woodhand(self):
        """点木手"""
        return self.category == Static.ITEM_TYPE_WOODHAND

    @property
    def is_equiprefinestone(self):
        """装备精炼石"""
        return self.category == Static.ITEM_TYPE_EQUIPREFINESTONE

    @property
    def is_materialcore(self):
        """元素之核"""
        return self.category == Static.ITEM_TYPE_MATERIALCORE

    @property
    def is_package_all(self):
        """多选包"""
        return self.category == Static.ITEM_TYPE_PACEKAGE_ALL

    @property
    def is_package_single(self):
        """单选包"""
        return self.category == Static.ITEM_TYPE_PACEKAGE_SINGLE

    @property
    def is_fruit_flower(self):
        """花的果实"""
        return self.category == Static.ITEM_TYPE_FRUIT_FLOWER

    @property
    def is_fruit_tree(self):
        """树的果实"""
        return self.category == Static.ITEM_TYPE_FRUIT_TREE  

    def goldhand_gold(self, player, buy_count, price):
        """根据元宝数量获取金币"""
        if buy_count > 34:
            gold = 800
            # 上面的gold 是钻石和金币的比例,price是钻石的价格。总金币获得量是钻石×金币比例
            gold = gold * price
            probalities = Static.ITEM_GOLDHAND_INFO
            ratio, _ = random_item_pick(probalities)
            return ratio, ratio * gold

        else:
            ratio = 1
            from module.building.api import get_buildinggoldhand

            goldhang_info = get_buildinggoldhand(buy_count + 1)
            properb = random.randint(1, 10000)
            if properb <= goldhang_info.critProperbility:
                critProper = random.randint(1, 100)
                if critProper <= goldhang_info.critTwo:
                    ratio = 2
                elif critProper <= goldhang_info.critThree:
                    ratio = 3
                elif critProper <= goldhang_info.critFive:
                    ratio = 5
                elif critProper <= goldhang_info.critTen:
                    ratio = 10

            gold = goldhang_info.expectGold

            return ratio, ratio * gold

    def woodhand_wood(self, buy_count):
        """根据元宝数量获取"""
        wood = 1000 - (float(buy_count)/(buy_count + 20)) * 1000 # 3.20更改

        # wood = 1000 + player.level * 100
        # wood += wood * buy_count * 0.05
        # wood = int(wood)
        # probalities = Static.ITEM_WOODHAND_INFO

        # ratio, _ = random_item_pick(probalities)
        # yoyprint(u"wood hand ratio is %s, base number is %s buy count is %s level is %s" % (ratio, wood, buy_count, player.level))
        return 0, wood

    @memoized_property
    def rewards(self):
        from rewards.api import get_commonreward
        return [get_commonreward(pk) for pk in self.rewardIds_str.strip().split(",") if pk]

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = self.pk
        del dicts["id"]
        del dicts["name"]
        del dicts["description"]
        return dicts

class Store(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"商店"
    name = models.CharField(u"name", max_length=200, default=0)
    nameId = models.CharField(u"goodsName", max_length=200, default=0)
    baseDiamond = models.IntegerField(u"基础价格", default=0)
    incrDiamond = models.IntegerField(u"购买价格上升", default=0)
    dailyCount = models.IntegerField(u"每日限购上限",default=0)
    item_id = models.IntegerField(u"item",default=0)
    display = models.BooleanField(u"是否显示", default=True)
    orderId = models.IntegerField(u"排序", default=0)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()

        dicts["itemId"] = dicts["item_id"] 
        dicts["gid"] = dicts["id"] 
        del dicts["id"]
        del dicts["name"]
        del dicts["item_id"]
        return dicts

    @property
    def is_limitbuy(self):
        return self.dailyCount != 0

    @memoized_property
    def item(self):
        return Item.get(self.item_id)

class ItemCompose(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"物品合成"
    _CACHE_FKS = ["itemId"]
    name = models.CharField(u"name", max_length=200, default=0)
    pos = models.IntegerField(u"部位ID", default=0)
    searchDifficuty_int = models.CharField(u"掉落关卡难度", max_length=200, default="")
    searchInstances_int = models.CharField(u"掉落关卡", max_length=200, default="")
    icon = models.CharField(u"icon", max_length=200, default="")
    nameId = models.CharField(u"nameId", max_length=200, default="")
    itemId = models.IntegerField(u"合成后物品ID", default=0)
    fragmentId = models.IntegerField(u"物品ID", default=0)
    descriptionId = models.CharField(u"descriptionId", max_length=200, default="")
    num = models.IntegerField(u"需要碎片数量", default=0)
    type = models.IntegerField(u"类型前端分页", default=0)
    orderId = models.IntegerField(u"id前端分页", default=0)

    @classmethod
    def get_itemcomposes_by_item_id(cls, item_id):
        _cache_data = cls.get_list_by_foreignkey("itemId")
        return _cache_data[str(item_id)] if str(item_id) in _cache_data else {}

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = self.pk
        del dicts["id"]
        del dicts["name"]
        return dicts

class CouragePointStore(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"勇气商店"
    couragepoint = models.IntegerField(u"勇气点数量",default=0)
    item_id = models.IntegerField(u"物品碎片ID",default=0)
    count = models.IntegerField(u"数量",default=0)
    orderId = models.IntegerField(u"排序", default=0)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()

        dicts["pk"] = dicts["id"] 
        dicts["couragePoint"] = self.couragepoint
        dicts["itemId"] = self.item_id
        del dicts["id"]
        del dicts["couragepoint"]
        del dicts["item_id"]
        return dicts

    @memoized_property
    def item(self):
        return Item.get(self.item_id)


class TowerStore(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"爬塔商店"
    name = models.CharField(u"name", max_length=200, default=0)
    nameId = models.CharField(u"goodsName", max_length=200, default=0)
    basePrice = models.IntegerField(u"基础价格", default=0)
    incrPrice = models.IntegerField(u"购买价格上升", default=0)
    dailyCount = models.IntegerField(u"每日限购上限",default=0)
    item_id = models.IntegerField(u"item",default=0)
    display = models.BooleanField(u"是否显示", default=True)
    orderId = models.IntegerField(u"排序", default=0)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()

        dicts["itemId"] = dicts["item_id"]
        dicts["gid"] = dicts["id"]
        del dicts["id"]
        del dicts["name"]
        del dicts["item_id"]
        return dicts

    @property
    def is_limitbuy(self):
        return self.dailyCount != 0

    @memoized_property
    def item(self):
        return Item.get(self.item_id)
