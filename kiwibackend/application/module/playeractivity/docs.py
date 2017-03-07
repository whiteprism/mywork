# -*- coding: utf-8 -*-
from mongoengine import *
from common.docs import PlayerRedisDataBase
from common.decorators.memoized_property import memoized_property
from activity.models import Activity
import datetime
from module.common.static import Static
from module.vip.api import get_vip


class PlayerActivity(PlayerRedisDataBase):
    """
    用户活动奖励数据
    """
    valueIntArray = ListField(default = []) #领取的结构
    received = BooleanField(default=False) #是否已经领取该奖励
    getTime = DateTimeField(default=datetime.datetime.min) #领取时间,备用
    endTime = DateTimeField(default=datetime.datetime.min) #备用 , 月卡到期时间
    value1 = IntField(default=0) #字段1 {登录奖励:代表累计登录天数}
    value2 = IntField(default=0) #备用字段1, 月卡是否可以领取 1 = 可以， 0 不可以
    value3 = IntField(default=0) #备用字段1, 0, 没有领取过， 1=已经领取过了

    def __unicode__(self):
        return u"%s:%s" %(self.id, self.pk)

    def new(self, player):
        super(self.__class__, self).new(player)
        if self.activity.isCountinueLogin:
            self.value1 = 1

    @memoized_property
    def activity(self):
        return Activity.get(self.pk)

    @property
    def activityType(self):
        return self.activity.category

    def checkGet(self, valueInt):
        '''
        检测没有领取过该奖励
        '''
        if valueInt in self.valueIntArray:
            return False
        return True

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["otherView"] = {"hasGotReward": self.received}
        dicts["isFinish"] = not self.activity.isOpen(self.player.userid)
        dicts["actitityType"] = self.activityType
        dicts["data"] = self.data
        dicts["activityId"] = self.pk
        del dicts["valueIntArray"]
        del dicts["getTime"]
        del dicts["endTime"]
        del dicts["received"]
        del dicts["id"]
        return dicts

    @property
    def data(self):
        '''
        前端需要数据
        '''
        return {"entry":[{"valueIntArray":self.valueIntArray}]} #前端messagepack用格式

    def get_login_boxrewards(self, rule_value):
        activity = self.activity 

        check_n = self.value1

        if not self.received:
            check_n -= 1#今天没有领取，比对时间减少1天

        rewards = []
        if rule_value <= check_n and rule_value not in self.valueIntArray:
            for rule in activity.rules:
                if rule.value1 == rule_value:
                    rewards = rule.giftPackage.boxRewards
                    self.valueIntArray.append(rule_value)
                    self.player.update_activity(self, True)
                    break

        return rewards


    def get_rewards(self, rule_value):
        '''
        获得奖励
        '''
        is_right = False
        rewards = []
        data = {}
        number = 1
        activity = self.activity 
        #签到
        if activity.isCountinueLogin:
            if rule_value == self.value1:
                if not self.received:
                    self.received = True
                    self.getTime = datetime.datetime.now()
                    self.player.update_activity(self, True)
                    #vip 等级高，奖励多倍
                    for rule in activity.rules:
                        if rule.value1 == rule_value:
                            rewards = rule.giftPackage.rewards
                            if self.player.vip_level >= rule.value2:
                                number = rule.value3
                            is_right = True
                            break

        #新手等级
        elif activity.isNewerLevel:
            if rule_value <= self.player.level and rule_value not in self.valueIntArray:
                if self.checkGet(rule_value):
                    for rule in activity.rules:
                        if rule.value1 == rule_value:
                            rewards = rule.giftPackage.rewards
                            self.valueIntArray.append(rule_value)
                            self.player.update_activity(self, True)
                            is_right = True
                            break

        #用户成长
        elif activity.isUserGrowUp:
            #可能逻辑不同，分开写吧
            if self.received:
                if rule_value <= self.player.level and rule_value not in self.valueIntArray:
                    if self.checkGet(rule_value):
                        for rule in activity.rules:
                            if rule.value2 == rule_value:
                                rewards = rule.giftPackage.rewards
                                self.valueIntArray.append(rule_value)
                                self.player.update_activity(self, True)
                                is_right = True
                                break
            else:
                vip = get_vip(self.player.vip_level)
                if vip.growthFund and self.player.yuanbo >= Static.GROW_GOLD_ACTIVITY_MOJO:
                    self.player.sub_yuanbo(Static.GROW_GOLD_ACTIVITY_MOJO, info=u"成长基金")
                    self.received = True
                    self.player.update_activity(self, True)

        if not is_right:
            rewards = []
        data["rewards"] = rewards
        data["number"] = number
    
        return data
