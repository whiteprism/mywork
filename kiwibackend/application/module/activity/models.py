# -*- coding: utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler
from rewards.models import RewardsBase
from module.common.static import Static
from common.decorators.memoized_property import memoized_property
import datetime
from module.experiment.api import get_experiment, check_player_in_experiment_by_experiment

class Activity(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"活动"
    nameId = models.CharField(u"名字", max_length=100, default="") #名字
    iconId = models.CharField(u"图标", max_length=100, default="") #名字
    category = models.IntegerField(u"活动类型", default=0) #1001 --- 1010
    experimentName = models.CharField(u"实验名", max_length=100, default="") #名字

    def __unicode__(self):
        return u"%s:%s" %(self.pk, self.category)

    class Meta:
        ordering = ["id"]

    def isOpen(self, userid):
        '''
        是否在活动时间内
        '''
        if not self.experimentName:
             return True

        experiment = get_experiment(self.experimentName)
        return check_player_in_experiment_by_experiment(userid, experiment)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["rules"] = [rule.to_dict() for rule in self.rules]
        return dicts

    @property
    def isCountinueLogin(self):
        return self.category == Static.CONTINUOUS_LOGIN_TYPE

    @property
    def isNewerLevel(self):
        return self.category == Static.NEWER_LEVEL_TYPE

    @property
    def isUserGrowUp(self):
        return self.category == Static.USER_GROW_UP

    @property
    def rules(self):
        '''
        所有规则
        '''
        all_rules = ActivityRule.get_rule_by_activity(self)
        return all_rules

class ActivityRule(models.Model, StaticDataRedisHandler, CommonStaticModels):
    _CACHE_FKS = ["activityId"]
    SHEET_NAME = u"活动规则"
    activityId = models.IntegerField(u"活动的id(Activity id)", default=0)
    giftBagId = models.IntegerField(u"礼包奖励gid", default=0)
    value1 = models.IntegerField(u"valueInt", default=0)
    value2 = models.IntegerField(u"备用字段2", default=0)
    value3 = models.IntegerField(u"备用字段3", default=0)
    value4 = models.IntegerField(u"备用字段4", default=0)
    value5 = models.IntegerField(u"备用字段5", default=0)
    value6 = models.IntegerField(u"备用字段6", default=0)

    

    @memoized_property
    def activity(self):
        return Activity.get(self.activityId)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        gift_package = self.giftPackage
        dicts["giftBag"] = gift_package.to_dict() if gift_package else {}
        return dicts

    @classmethod
    def get_rule_by_activity(cls, activity_or_acitivity_id):
        if isinstance(activity_or_acitivity_id, Activity):
            activity_id = activity_or_acitivity_id.pk
        else:
            activity_id = int(activity_or_acitivity_id)

        _cache_data = cls.get_list_by_foreignkey("activityId")
        return _cache_data[str(activity_id)] if str(activity_id) in _cache_data else {}

    @memoized_property
    def giftPackage(self):
        return GiftPackage.get(self.giftBagId)

class GiftPackage(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"活动奖励"
    category = models.IntegerField(u"活动类型", default=0) #1001 --- 1010
    name = models.CharField(u"名字", max_length=100) #名字
    entryName_key = models.CharField(u"entry名字key", max_length=100) #登记的名字???
    entryName_val = models.CharField(u"entry名字value", max_length=100) #登记的名字???
    level = models.IntegerField(u"等级", default=0)
    rewards_int = models.CharField(u"奖励的id list", max_length = 200, default="")
    #签到专用
    boxRewards_int = models.CharField(u"奖励ID", max_length=100, default=0)
    boxPrecent = models.IntegerField(u"位置", default=0)
    boxImgs_str = models.CharField(u"宝箱图集", max_length=100, default=0)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["rewards"] = [reward.to_dict() for reward in self.rewards]
        dicts["boxRewards"] = [reward.to_dict() for reward in self.boxRewards]
        dicts["boxImgs"] = self.boxImgs_str.strip().split(",") 
        dicts["entryName"] = [{"key" : self.entryName_key, "value" : self.entryName_val}]
        dicts["pk"] = self.id
        del dicts["entryName_key"]
        del dicts["entryName_val"]
        del dicts["id"]
        return dicts

    @memoized_property
    def boxRewards(self):
        return [ActivityReward.get(int(float(reward_id))) for reward_id in self.boxRewards_int.strip().split(",") if reward_id]

    @memoized_property
    def rewards(self):
        '''
        获得奖励
        '''
        return [ActivityReward.get(int(float(i))) for i in self.rewards_int.strip().split(",") if i]

class ActivityReward(RewardsBase):
    SHEET_NAME = u"活动奖励列表"
