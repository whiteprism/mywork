# -*- coding: utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler
from rewards.models import RewardsBase
from common.decorators.memoized_property import memoized_property
import datetime

class Package(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"礼包"
    id = models.CharField("礼包ID", max_length=30, primary_key=True)
    name = models.CharField(u"礼包标示", max_length=20, default="")
    batch = models.CharField(u"批次", max_length=20, default="")
    rewards_int = models.CharField(u"奖励ID", max_length=100, default=0)
    channels_str = models.CharField(u"渠道ID", max_length=200, default=0)
    serverids_int = models.CharField(u"服务器ID", max_length=100, default=0)
    expire_date = models.CharField(u"过期时间", max_length=50, default=0)
    gift_title = models.CharField(u"礼物标题", max_length=100, default=0)
    gift_body = models.CharField(u"礼物内容", max_length=200, default=0)
    code_count = models.IntegerField(u"使用的用户ID", default=0)
    tag = models.CharField(u"生成路径", max_length=50, default=0)

    @memoized_property
    def expired_at(self):
        return datetime.datetime.strptime(self.expire_date,'%Y-%m-%d %H:%M:%S')

    @memoized_property
    def channels(self):
        return [channel for channel in self.channels_str.strip().split(",") if channel]

    @memoized_property
    def serverids(self):
        return [int(float(serverid)) for serverid in self.serverids_int.strip().split(",") if serverid]

    @memoized_property
    def rewards(self):
        return [PackageReward.get(int(float(reward_id))) for reward_id in self.rewards_int.strip().split(",") if reward_id]

class PackageCode(models.Model):
    """
    礼包编码
    """
    id = models.CharField("礼包编码", max_length=30, primary_key=True)
    package_id = models.CharField("礼包编码", max_length=30)
    is_use = models.BooleanField("是否使用", default=False)
    use_serverid = models.CharField(u"使用服务器ID", max_length=20, default="")
    use_playerid = models.IntegerField(u"使用的用户ID", default=0)
    created_at = models.DateTimeField("创建时间")
    used_at = models.DateTimeField("创建时间")

    @memoized_property
    def package(self):
        return Package.get(self.package_id)

    @property
    def is_expired(self):
        now = datetime.datetime.now()
        return now > self.package.expired_at
    
    def check_channel(self, channel):
        if self.package.channels and channel not in self.package.channels:
            return False

        return True

    def check_server(self, serverid):
        if self.package.serverids and serverid not in self.package.serverids:
            return False

        return True

class PackageReward(RewardsBase):
    """
    礼包奖励   
    """
    SHEET_NAME = u"礼包奖励"
