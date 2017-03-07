# -*- coding: utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler
from rewards.models import RewardsBase
from common.decorators.memoized_property import memoized_property
import datetime

class LoginBonus(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"连续登陆"
    rewards_int = models.CharField(u"奖励ID", max_length=100, default=0)
    gift_title = models.CharField(u"礼物标题", max_length=100, default=0)
    gift_body = models.CharField(u"礼物内容", max_length=200, default=0)
    

    @memoized_property
    def rewards(self):
        return [LoginBonusReward.get(int(float(reward_id))) for reward_id in self.rewards_int.strip().split(",") if reward_id]

class LoginBonusReward(RewardsBase):
    """
    连续登陆奖励   
    """
    SHEET_NAME = u"连续登陆奖励"
