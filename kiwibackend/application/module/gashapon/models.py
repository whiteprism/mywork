# -*- coding: utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler
from common.static import Static
from django.conf import settings
from rewards.models import RewardsBase
from hero.api import get_warrior
from soul.api import get_soul
from item.api import get_item
from equip.api import get_equip, get_equipfragment
from artifact.api import get_artifactfragment
#from gem.api import get_gem, get_gemfragment
from module.utils import random_item_pick 
from module.currency.models import Currency, get_currency
from common.decorators.memoized_property import memoized_property
from rewards.api import get_commonreward

class Tavern(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"抽奖入口"
    cdTime = models.IntegerField(u"cdTime",default=0)
    level = models.IntegerField(u"level",default=0)
    cost = models.IntegerField(u"cost",default=0)
    maxDailyCount = models.IntegerField(u"每日免费次数",default=0)
    tenCost = models.IntegerField(u"十连抽",default=0)
    discount = models.IntegerField(u"折扣",default=0)
    gashapon_id = models.IntegerField(u"对应抽奖ID",default=0)
    rewardId = models.CharField("单抽奖励", max_length=255)
    tenRewardId = models.CharField("十连抽奖励", max_length=255)

    @memoized_property
    def reward(self):
        return get_commonreward(self.rewardId)

    @memoized_property
    def tenReward(self):
        return get_commonreward(self.tenRewardId)

    @property
    def is_gold(self):
        return self.pk == Static.GASHAPON_GOLD

    @property
    def is_diamond(self):
        return self.pk == Static.GASHAPON_DIAMOND

    @memoized_property
    def costConf(self):
        if self.cost:
            return TavernCost.get(self.cost).to_dict()
        return None

    @memoized_property
    def tavern_cost(self):
        if self.cost:
            return TavernCost.get(self.cost)
        return None

    @memoized_property
    def tenCostConf(self):
        if self.tenCost:
            return TavernCost.get(self.tenCost).to_dict()
        return None

    @memoized_property
    def tavern_tencost(self):
        if self.tenCost:
            return TavernCost.get(self.tenCost)
        return None

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["cost"] =  self.costConf
        dicts["tenCost"] = self.tenCostConf
        del dicts["id"]
        del dicts["gashapon_id"]
        return dicts

class TavernCost(RewardsBase):
    SHEET_NAME = u"抽奖消耗"


class Gashapon(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"抽奖"
    name = models.CharField(u"抽奖名称",default="", max_length=200)
    topreward_number = models.SmallIntegerField(u"n次必出", default=0)
    topreward_rarity = models.SmallIntegerField(u"必出分类", default=0)
    topreward_quality = models.SmallIntegerField(u"必出稀有度", default=0)
    topreward_reset = models.BooleanField(u"必出后是否重置", default=False)
    description = models.CharField(u"描述", default="", max_length=200)

    def __unicode__(self):
        return u"%s:%s" %(self.name, self.id)

    #@property
    #def can_free(self):
    #    return self.number == 1

    @classmethod
    def create_cache(cls):
        super(Gashapon, Gashapon).create_cache()
        cls.GASHAPON_DATAS = {
            "gashapon_rarity_probabilities": {},
            "gashapon_probalities": {},
        }
        gashapons = cls.get_all_list()
        for gashapon in gashapons:
            _gashapon_id = str(gashapon.pk)
            cls.GASHAPON_DATAS["gashapon_rarity_probabilities"][_gashapon_id] = GashaponRarityProbability.get_gashapon_rarity_probability_by_gashapon(gashapon)
            
            _gashapon_probalities = GashaponProbability.get_gashapon_probability_by_gashapon(gashapon)
            gashapon_probalities = {}
            for p in _gashapon_probalities:

                _rarity = str(p.rarity)
                if _rarity not in gashapon_probalities:
                    gashapon_probalities[_rarity] = {}
                if p.gashapon_hero:
                    target = get_warrior(p.target_id)
                elif p.gashapon_soul:
                    target = get_soul(p.target_id)
                elif p.gashapon_equip:
                    target = get_equip(p.target_id)
                #elif p.gashapon_gem:
                #    target = get_gem(p.target_id)
                elif p.gashapon_item:
                    target = get_item(p.target_id)
                elif p.gashapon_artifactfragment:
                    target = get_artifactfragment(p.target_id)
                elif p.gashapon_equipfragment:
                    target = get_equipfragment(p.target_id)
                elif p.gashapon_currency:
                    target = get_currency(p.target_id)
                else:
                    raise


                _quality = str(target.quality)

                if _quality not in  gashapon_probalities[_rarity]:
                    gashapon_probalities[_rarity][_quality] = []
                gashapon_probalities[_rarity][_quality].append(p)
            cls.GASHAPON_DATAS["gashapon_probalities"][_gashapon_id] = gashapon_probalities
            if settings.ENABLE_REDIS_CACHE:
                cls.redis_set(cls.get_kvs_key("GASHAPON_DATAS"), cls.GASHAPON_DATAS)

    @classmethod
    def get_random_rarity(cls, gashapon, rarity=0, quality=0):
        _target_gashapon_id = str(gashapon.id)
        if not hasattr(cls, "GASHAPON_DATAS") or not cls.GASHAPON_DATAS:
            cls.GASHAPON_DATAS = None
            if settings.ENABLE_REDIS_CACHE:
                cls.GASHAPON_DATAS = cls.redis_get(cls.get_kvs_key("GASHAPON_DATAS"))
            if not cls.GASHAPON_DATAS:
                cls.create_cache()

        if not cls.GASHAPON_DATAS:
            return None

        if _target_gashapon_id not in cls.GASHAPON_DATAS["gashapon_rarity_probabilities"]:
            return None

        _gashapon_rarity_probabilities = cls.GASHAPON_DATAS["gashapon_rarity_probabilities"][_target_gashapon_id]

        if rarity and quality:
            gashapon_rarity_probabilities = [(p, p.probability) for p in _gashapon_rarity_probabilities if p.rarity == rarity and p.quality == quality]
        elif quality:
            gashapon_rarity_probabilities = [(p, p.probability) for p in _gashapon_rarity_probabilities if p.quality == quality]
        elif rarity:
            gashapon_rarity_probabilities = [(p, p.probability) for p in _gashapon_rarity_probabilities if p.rarity == rarity]
        else:
            gashapon_rarity_probabilities = [(p, p.probability) for p in _gashapon_rarity_probabilities]

        target_gashapon_rarity_probability, _ = random_item_pick(gashapon_rarity_probabilities)

        return target_gashapon_rarity_probability
       
        
    @classmethod
    def get_random_target(cls, gashapon, gashapon_rarity_probability):
        _target_gashapon_id = str(gashapon.id)
        _rarity = str(gashapon_rarity_probability.rarity)
        _quality = str(gashapon_rarity_probability.quality)

        if not hasattr(cls, "GASHAPON_DATAS") or not cls.GASHAPON_DATAS:
            cls.GASHAPON_DATAS = cls.redis_get(cls.get_kvs_key("GASHAPON_DATAS"))
            if not cls.GASHAPON_DATAS:
                cls.create_cache()

        if not cls.GASHAPON_DATAS:
            yoyprint(u"not gashapon datas")
            return None

        if _target_gashapon_id not in cls.GASHAPON_DATAS["gashapon_probalities"]:
            return None

        _gashapon_probabilities = cls.GASHAPON_DATAS["gashapon_probalities"][_target_gashapon_id]
        if _rarity not in  _gashapon_probabilities:
            yoyprint(u"not rarity %s" % _rarity)
            return None
        _gashapon_probabilities = _gashapon_probabilities[_rarity]

        if _quality not in _gashapon_probabilities:
            #print _gashapon_probabilities
            yoyprint(u"_rarity %s not quality %s" % (_rarity, _quality))
            return None

        _gashapon_probabilities = _gashapon_probabilities[_quality]

        gashapon_probabilities = [(p, p.probability) for p in _gashapon_probabilities]
        target, _ = random_item_pick(gashapon_probabilities)

        return target


class GashaponRarityProbability(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"抽奖类别概率"
    _CACHE_FKS = ["gashapon_id"]
    gashapon = models.ForeignKey(Gashapon)
    quality = models.SmallIntegerField(u"星级", default=0)
    rarity = models.SmallIntegerField(u"分类", default=1)
    probability = models.IntegerField(u"概率", default=0)

    def __unicode__(self):
        return u"%s:%s:%s(%s)" %(self.gashapon.name, self.rarity, self.quality, self.probability)

    def __getattribute__(self, name):
        if name == 'gashapon':
            return self._related_gashapon
        return object.__getattribute__(self, name)

    @classmethod
    def get_gashapon_rarity_probability_by_gashapon(cls, gashapon):
        _cache_data = cls.get_list_by_foreignkey("gashapon_id")
        return _cache_data[str(gashapon.id)] if str(gashapon.id) in _cache_data else {}

    @property
    def _related_gashapon(self):
        return Gashapon.get(self.gashapon_id)

    @property
    def gashaon_hero(self):
        return self.rarity == Static.GASHAPON_RARITY_HERO

    @property
    def gashapon_soul(self):
        return self.rarity == Static.GASHAPON_RARITY_SOUL

    @property
    def gashapon_equip(self):
        return self.rarity == Static.GASHAPON_RARITY_EQUIP

    @property
    def gashapon_item(self):
        return self.rarity == Static.GASHAPON_RARITY_ITEM


    @property
    def gashapon_equipfragment(self):
        return self.rarity == Static.GASHAPON_RARITY_EQUIPFRAGMENT

    @property
    def gashapon_artifactfragment(self):
        return self.rarity == Static.GASHAPON_RARITY_ARTIFACTFRAGMENT

    @property
    def gashapon_currency(self):
        """
        货币
        """
        return self.rarity == Static.GASHAPON_RARITY_CURRENCY

class GashaponProbability(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"抽奖概率"
    _CACHE_FKS = ["gashapon_id"]
    gashapon = models.ForeignKey(Gashapon)
    rarity = models.SmallIntegerField(u"分类")
    target_id = models.IntegerField(u"奖品")
    probability = models.IntegerField(u"概率")
    number = models.IntegerField(u"数量", default=0)

    def __unicode__(self):
        return u"%s:%s:%s(%s)" %(self.gashapon.name, self.rarity, self.target_id, self.probability)

    def __getattribute__(self, name):
        if name == 'gashapon':
            return self._related_gashapon
        return object.__getattribute__(self, name)

    @classmethod
    def get_gashapon_probability_by_gashapon(cls, gashapon):
        _cache_data = cls.get_list_by_foreignkey("gashapon_id")
        return _cache_data[str(gashapon.id)] if str(gashapon.id) in _cache_data else {}
    

    @property
    def _related_gashapon(self):
        return Gashapon.get(self.gashapon_id)

    @property
    def gashapon_hero(self):
        return self.rarity == Static.GASHAPON_RARITY_HERO

    @property
    def gashapon_soul(self):
        return self.rarity == Static.GASHAPON_RARITY_SOUL

    @property
    def gashapon_equip(self):
        return self.rarity == Static.GASHAPON_RARITY_EQUIP

    @property
    def gashapon_item(self):
        return self.rarity == Static.GASHAPON_RARITY_ITEM

    #@property
    #def gashapon_gem(self):
    #    return self.rarity == Static.GASHAPON_RARITY_GEM

    #@property
    #def gashapon_gemfragment(self):
    #    return self.rarity == Static.GASHAPON_RARITY_GEMFRAGMENT

    @property
    def gashapon_artifactfragment(self):
        return self.rarity == Static.GASHAPON_RARITY_ARTIFACTFRAGMENT

    @property
    def gashapon_equipfragment(self):
        return self.rarity == Static.GASHAPON_RARITY_EQUIPFRAGMENT

    @property
    def gashapon_currency(self):
        return self.rarity == Static.GASHAPON_RARITY_CURRENCY
