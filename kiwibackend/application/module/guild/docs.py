# -*- coding: utf-8 -*-
from mongoengine import *
from common.decorators.memoized_property import memoized_property, memoized_property_delete
from module.item.api import get_item
import datetime, time
from utils import datetime_to_unixtime
from common.docs import PlayerDataBase, PlayerRelationBase, PlayerRedisDataBase, PlayerModifyBase, PlayerRedisDataModifyBase
import random
from module.vip.api import get_vip
from module.common.actionlog import ActionLogWriter
from module.common.static import Static
from submodule.fanyoy import short_data
from module.instance.api import get_guildinstancelevel
from django.conf import settings
from submodule.fanyoy.redis import StaticSetDataRedisHandler,StaticListRedisHandler

class PlayerGuildShop(PlayerRedisDataBase):
    """
    用户公会商店信息
    """
    buyItem = ListField(default=[]) #已经购买item
    #refreshCount = IntField(default=0) #免费今日刷新次数 
    #diamondRefreshCount = IntField(default=0) #元宝今日刷新次数
    shopItem = ListField(default=[]) #可以购买item
    autoRefreshAt = DateTimeField(default=datetime.datetime.now)
    #refreshAt = DateTimeField(default=datetime.datetime.now)
    REFRESH_HOURS = [20, 8]
    
    def new(self, player):
        super(self.__class__, self).new(player)
        self.refresh()
        
    def load(self, player):
        super(self.__class__, self).load(player)
        #now = datetime.datetime.now()
        self.refresh_auto()
        #if self.refreshAt.date() != now.date():
            #self.refreshCount = 0
            #self.diamondRefreshCount = 0
            #self.update()
        #    return True
        #return False

    #@classmethod
    #def _before_refresh_hour(cls, hour):
    #    for _h in cls.REFRESH_HOURS:
    #        if _h < hour:
    #            return _h
    #    return _h

    # @classmethod
    # def _next_refesh_hour(cls, hour):
    #     before_hour = cls._before_refresh_hour(hour)
    #     _index = cls.REFRESH_HOURS.index(before_hour)
    #     return cls.REFRESH_HOURS[_index-1]
        
    @property
    def leftRefreshTime(self):
        """
        剩余自动刷新时间
        """
        now = datetime.datetime.now()

        #next_refesh_hour = PlayerGuildShop._next_refesh_hour(now.hour)
        # if next_refesh_hour < now.hour:
        #     end_time = datetime.datetime(now.year, now.month, now.day, next_refesh_hour, 59, 59) + datetime.timedelta(1)
        # else:
        #     end_time = datetime.datetime(now.year, now.month, now.day, next_refesh_hour, 59, 59)
        end_time = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)
        return int(( end_time - now ).total_seconds() + 4)

    def refresh_auto(self):
        now = datetime.datetime.now()
        if self.autoRefreshAt.date() == now.date():
            #if PlayerGuildShop._before_refresh_hour(self.autoRefreshAt.hour)  ==  PlayerGuildShop._before_refresh_hour(now.hour):
            return False
        #else:
            #0点更新
        #    self.refreshCount = 0
        #    self.diamondRefreshCount = 0
        self.autoRefreshAt = now
        self.refresh()
        return True

    def _refresh_normal(self):
        from guild.models import GuildShop
        # 刷新不分普通还是高级ｖｉｐ　统一显示最多
        normal_show_ids = GuildShop.normal_show_ids()


        for show_id, number in normal_show_ids:
            shopitems = GuildShop.get_items_by_show_id(show_id)

            if not shopitems:
                break

            sample_shopitems = random.sample(shopitems, number)
            for _shopitem in sample_shopitems:
                self.shopItem.append(_shopitem.pk)

        return True

    def refresh(self):
        self.buyItem = []
        self.shopItem = []

        self._refresh_normal()

        self.update()
        return True
        
    def can_buy(self, shop_id):
        shop_id = int(shop_id)
        if shop_id not in self.shopItem:
            return False
        if shop_id in self.buyItem:
            return False
        return True

    def buy(self, shop_id):
        shop_id = int(shop_id)
        self.buyItem.append(shop_id)
        self.update()

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        del_keys = ["id", "autoRefreshAt"]
        for del_key in del_keys:
            if del_key in dicts:
                del dicts[del_key]
        dicts["leftRefreshTime"] = self.leftRefreshTime

        return dicts

class PlayerGuild(PlayerRedisDataModifyBase):
    """
    玩家公会信息
    """
    position = IntField(default = 0) # 公会等级
    gold = IntField(default = 0) # 公会币
    guildId = IntField(default = 0) # 公会ID
    leftAt = DateTimeField(default=datetime.datetime(2016,9,1)) 
    readAttV = IntField(default = 0) # 读取最新的公会公告版本
    dailyContributionXp = IntField(default = 0) #今天贡献经验
    totalContributionXp = IntField(default = 0)  #一共贡献经验
    totalContribution = IntField(default = 0)  #总贡献度
    #maxContributionCount = IntField(default = 5) #最大有效贡献次数
    dailyContributionCount = IntField(default = 0)  #今日有效贡献次数
    dailyCostContributionCount = IntField(default = 0)  #今日非有效贡献次数
    trainingHeroIds = ListField(default=[0,0,0,0,0,0,0,0]) # 公会训练场的英雄
    speedPlayerIds = ListField() #赠送药水用户
    speededPlayerIds = ListField() #被赠送的用户药水

    #def canJoinGuid(self, guild):
    #def joinGuid(self, guild):
    #    """
    #    加入公会
    #    """

    def load(self, player):
        super(self.__class__, self).load(player)
        now = datetime.datetime.now()
        if self.updated_at.date() != now.date():
            self.dailyContributionXp = 0 #今天贡献经验
            self.dailyContributionCount = 0
            self.speedPlayerIds = []
            self.speededPlayerIds = []
            return True
        return False

    @property
    def isChairman(self):
        """
        会长
        """
        return self.position == Static.GUILD_CHAIRMAN_POSITION

    @property
    def isViChairman(self):
        """
        副会长
        """
        return self.position == Static.GUILD_VI_CHAIRMAN_POSITION

    @property
    def isMember(self):
        """
        成员
        """
        return self.position == Static.GUILD_NORMAL_POSITION

    @property
    def maxContributionCount(self):
        return 5

    @property
    def isMaxSpeeded(self):
        return len(self.speededPlayerIds) >= self.speededMaxCount

    @property
    def isMaxSpeed(self):
        return len(self.speedPlayerIds) >= self.speedMaxCount

    @property
    def speedMaxCount(self):
        return 5

    @property
    def speededMaxCount(self):
        return 5

    @property
    def dailyLeftContributionCount(self):
        """
        每天剩余贡献次数
        """
        return self.maxContributionCount - self.dailyContributionCount if self.maxContributionCount - self.dailyContributionCount > 0 else 0

    def add_gold(self, gold, info=u""):
        before_number = self.gold
        self.gold += gold
        after_number = self.gold
        ActionLogWriter.guild_add(self.player, before_number, after_number, gold, info)
        self.update()
        return True

    def sub_gold(self, gold, info=u""):
        if self.gold < gold:
            return False
        before_number = self.gold
        self.gold -= gold
        after_number = self.gold
        ActionLogWriter.guild_cost(self.player, before_number, after_number, gold, info)
        self.update()
        return True

    @memoized_property
    def guildInfo(self):
        if self.guildId > 0 :
            return SysGuildInfo.get_guild(self.guildId)
        return None

    def create_guild(self, guildName,  icon=0, limitLevel=0, category=0):
        """
        创建公会
        """
        guildinfo = SysGuildInfo(
            player_id=self.player.pk, 
            name = guildName,
            chairmanId = self.player.pk,
            icon = icon,
            membersIds = [self.player.pk],
            limitLevel = limitLevel,
            category = category,
            attention = "fytext_300766",
            outerAttention = "fytext_300765",
            serverid = settings.SERVERID,
        )
        guildinfo.save()

        self.position  =  Static.GUILD_CHAIRMAN_POSITION
        self.guildId = guildinfo.pk
        self.update()

    def join_guild(self, guildInfo):
        """
        加入公会
        """
        self.position = Static.GUILD_NORMAL_POSITION
        self.guildId = guildInfo.pk
        self.update()

        guildInfo.membersIds.append(self.player.pk)
        guildInfo.set_modify("membersIds")
        guildInfo.save()
        SysGuildInfo.release_lock(guildInfo.pk)

    def allow_join_guild(self, targetPlayer):
        """
        允许加入公会
        """
        targetPlayer.guild.position = Static.GUILD_NORMAL_POSITION
        targetPlayer.guild.guildId = self.guildInfo.pk
        targetPlayer.guild.update()
        SysGuildInfo.release_lock(guildInfo.pk)
        targetPlayer.passive_update()
        self.guildInfo.membersIds.append(targetPlayer.pk)
        self.guildInfo.set_modify("membersIds")
        self.guildInfo.requestMemberIds.remove(targetPlayer.pk)
        self.guildInfo.set_modify("requestMemberIds")


    def disallow_join_guild(self, targetPlayerId=None):
        """
        拒绝加入公会 or 已经加入其它公会
        """
        if targetPlayerId:
            self.guildInfo.requestMemberIds.remove(targetPlayerId)
        else:
            self.guildInfo.requestMemberIds = []
        self.guildInfo.set_modify("requestMemberIds")

    def request_guild(self, guildInfo):
        """
        加入公会
        """
        guildInfo.requestMemberIds.append(self.player.pk)
        guildInfo.set_modify("requestMemberIds")
        guildInfo.save()

    def change_position(self, targetPlayer, position):
        if position == Static.GUILD_VI_CHAIRMAN_POSITION:
            self.guildInfo.viChairmanIds.append(targetPlayer.pk)
            self.guildInfo.save()
            targetPlayer.guild.position = position
            targetPlayer.guild.update()
            targetPlayer.passive_update()
        elif position ==  Static.GUILD_NORMAL_POSITION:
        
            self.guildInfo.viChairmanIds.remove(targetPlayer.pk)
            self.guildInfo.save()

            targetPlayer.guild.position = position
            targetPlayer.guild.update()
            targetPlayer.passive_update()
        self.guildInfo.set_modify("viChairmanIds")
        self.guildInfo.set_modify("membersIds")

            
    def exchange_position(self, targetPlayer):
        
        guildInfo = self.guildInfo
        guildInfo.viChairmanIds.remove(targetPlayer.pk)
        guildInfo.chairmanId = targetPlayer.pk

        targetPlayer.guild.position = Static.GUILD_CHAIRMAN_POSITION
        targetPlayer.guild.update()
        targetPlayer.passive_update()
        
        self.player.guild.position = Static.GUILD_VI_CHAIRMAN_POSITION
        guildInfo.viChairmanIds.append(self.player.pk)
        self.player.guild.update()
        guildInfo.save()
        guildInfo.set_modify("viChairmanIds")
        guildInfo.set_modify("membersIds")

    def dissolve_guild(self):
        """
        解散公会
        """
        SysGuildInstanceInfo.objects.filter(guildId=self.guildId).delete()
        GuildAuctionsMaxInfo.objects.filter(guildId=self.guildId).delete()
        GuildLogInfo.objects.filter(guildId=self.guildId).delete()
        for membersId in self.guildInfo.membersIds:
            # 删除成员在公会战的配兵
            try:
                GuildSiegeConfigInfo.objects.get(player_id = membersId).delete()
            except:
                continue
        now = datetime.datetime.now()
        year, week, day = now.isocalendar()
        try:
            guildSiegeInfo = GuildSiegeInfo.objects.get(pk=week)
            if self.guildId in guildSiegeInfo.guildIds:
                guildSiegeInfo.guildIds.remove(self.guildId)
                guildSiegeInfo.save()
        except:
            pass

        self.quit_guild()

        self.guildInfo.delete()
        memoized_property_delete(self, "guildInfo")

    def quit_guild(self):
        """
        退出公会
        """
        if self.player.pk in self.guildInfo.viChairmanIds:
            self.guildInfo.viChairmanIds.remove(self.player.pk)
            self.guildInfo.set_modify("viChairmanIds")

        self.guildInfo.membersIds.remove(self.player.pk)
        self.guildInfo.set_modify("membersIds")
        self.guildInfo.save()

        self.position = 0
        self.guildId = 0
        self.leftAt = datetime.datetime.now()
        self.readAttV = 0
        self.dailyContributionXp = 0
        self.totalContributionXp = 0
        self.dailyContributionCount = 0
        for _playerHeroId in self.trainingHeroIds:
            if _playerHeroId > 0:
                _playerHero = self.player.heroes.get(_playerHeroId)
                if _playerHero:
                    _playerHero.untraining()
                    self.player.update_hero(_playerHero, True)

        self.trainingHeroIds = [0,0,0,0,0,0,0,0]
        # 将退出公会玩家 从公会团战战力中去掉
        try:
            GuildSiegeConfigInfo.objects.get(pk=self.player.pk).delete()
        except:
            pass
        self.update()

        return True

    def kick_from_guild(self, targetPlayer):
        """
        提出公会
        """

        if targetPlayer.pk in self.guildInfo.viChairmanIds:
            self.guildInfo.viChairmanIds.remove(targetPlayer.pk)
            self.guildInfo.set_modify("viChairmanIds")

        self.guildInfo.membersIds.remove(targetPlayer.pk)
        self.guildInfo.set_modify("membersIds")
        self.guildInfo.save()

        targetPlayer.guild.position = 0
        targetPlayer.guild.guildId = 0
        targetPlayer.guild.leftAt = datetime.datetime.now()
        targetPlayer.guild.readAttV = 0
        targetPlayer.guild.dailyContributionXp = 0
        targetPlayer.guild.totalContributionXp = 0
        targetPlayer.guild.dailyContributionCount = 0
        for _playerHeroId in targetPlayer.guild.trainingHeroIds:
            if _playerHeroId > 0:
                _playerHero = targetPlayer.heroes.get(_playerHeroId)
                if _playerHero:
                    _playerHero.untraining()
                    targetPlayer.update_hero(_playerHero, True)

        targetPlayer.guild.trainingHeroIds = [0,0,0,0,0,0,0,0]
        # 从公会团战战力中去掉
        try:
            GuildSiegeConfigInfo.objects.get(pk=self.player.pk).delete()
        except:
            pass
        targetPlayer.guild.update()
        targetPlayer.passive_update()

        return True

    def contribute(self, isValid, category, xp, gold, info):
        """
        贡献
        """
        if isValid:
            if xp > 0:
                today = datetime.datetime.now().date()
                if self.updated_at.date() != today:
                    self.dailyContributionCount = 0
                    self.dailyContributionXp = 0

                self.dailyContributionCount += 1
                self.dailyContributionXp += xp
                self.totalContributionXp += xp
                if category == 1:
                    self.totalContribution += Static.GUILD_GOLD_GET_CONTRIBUTION
                if category == 2:
                    self.totalContribution += Static.GUILD_DIAMOND_GET_CONTRIBUTION
                self.add_gold(gold, info) 
                self.guildInfo.contribute(xp)
                self.update()
                self.guildInfo.save()
        else:
            self.totalContribution += Static.GUILD_DIAMOND_GET_CONTRIBUTION + self.dailyCostContributionCount
            self.dailyCostContributionCount += 1
            self.add_gold(gold, info) 
            #self.guildInfo.contribute(xp)
            self.update()
            #self.guildInfo.save()

    def contribute_wood(self, wood):
        """
        捐献木材
        """
        self.guildInfo.wood += wood
        self.guildInfo.save()

    def level_up(self, guildLevel):
        """
        公会升级
        """

        self.guildInfo.level_up(guildLevel)

    def training_hero(self, playerHero, position):
        """
        训练英雄
        """
        playerHero.training()
        self.player.update_hero(playerHero, True)

        self.trainingHeroIds[position-1] = playerHero.pk
        self.set_modify("trainingHeroIds")
        self.update()

    def untraining_hero(self, playerHero):
        """
        解除训练英雄
        """
        playerHero.untraining()
        self.player.update_hero(playerHero, True)
        index = self.trainingHeroIds.index(playerHero.pk)
        self.trainingHeroIds[index] = 0
        self.set_modify("trainingHeroIds")
        self.update()

    def speed(self, targetPlayer):
        """
        加送（赠送药水）
        """
        self.speedPlayerIds.append(targetPlayer.pk)
        self.set_modify("speedPlayerIds")
        self.update()

        targetPlayer.guild.speededPlayerIds.append(self.player.pk)
        #self.guildInfo.set_modify("membersIds")#重新获取玩家数据
        targetPlayer.guild.update()
        targetPlayer.passive_update()

    @property
    def canJoinGuildAt(self):
        return datetime_to_unixtime(self.leftAt) # + datetime.timedelta(1))

    @property
    def hasRead(self):
        guildInfo = self.guildInfo
        if guildInfo:
            return self.readAttV == guildInfo.attentionV
        else:
            return True


    def userGuild_dict(self, guildInfo):
        '''
        获取公会展示数据
        '''
        dicts = {}
        player = self.player
        dicts["icon"] = player.iconId
        dicts["name"] = player.name
        dicts["vip"] = player.vip_level
        dicts["level"] = player.level
        dicts["id"] = player.id
        dicts["loginAt"] = int(time.time() - datetime_to_unixtime(player.updated_at))
        dicts["powerRank"] = player.powerRank
        dicts["heros"] = player.layoutHeroSimple_dict()
        dicts["dailyContributionXp"] = self.dailyContributionXp
        dicts["totalContributionXp"] = self.totalContributionXp
        dicts["totalContribution"] = self.totalContribution
        dicts["lastInstanceLevelId"] = player.lastInstance["lastLevelId"]
        if guildInfo.chairmanId == player.id:
            dicts["position"] = Static.GUILD_CHAIRMAN_POSITION
        elif player.id in guildInfo.viChairmanIds:
            dicts["position"] = Static.GUILD_VI_CHAIRMAN_POSITION
        else:
            dicts["position"] = Static.GUILD_NORMAL_POSITION

        return dicts

    def getFeiBookInfo(self):
        dicts = {"feiInstanceId": ""}
        guildinfo = self.guildInfo
        if  guildinfo:
            _feiBookInfo = None
            if str(self.player.id) in guildinfo.feiBookDict:
                feiBookInfo = guildinfo.feiBookDict[str(self.player.id)]    
                _feiBookInfo = sorted(feiBookInfo.iteritems(), key = lambda asd:asd[1])[0]
            dicts["feiInstanceId"] = _feiBookInfo[0] if _feiBookInfo else ""
        return dicts

    def to_dict(self, is_all=False, is_root=False):
        now = datetime.datetime.now()
        if now.date() != self.updated_at.date():
            self.dailyCostContributionCount = 0
            
        dicts = super(self.__class__, self).to_dict(is_all)

        relation_keys = {
            "maxContributionCount": [],
            "speedMaxCount": [],
            "speededMaxCount": [],
            "canJoinGuildAt": ["leftAt"],
            "hasRead": ["readAttV"],
        }

        for relation_key, key_list in relation_keys.items():
            if is_all or list(set(key_list).intersection(set(self.mKeys))):
                dicts[relation_key] = getattr(self, relation_key)
                if not is_all:
                    dicts["mKeys"].append(relation_key)

        guildinfo = self.guildInfo
        if  guildinfo:
            dicts["guildInfo"] = guildinfo.to_dict(is_all, is_root)
            if not is_all:
                dicts["mKeys"].append("guildInfo")
        elif not guildinfo:
            dicts["guildInfo"] = None
            if not is_all:
                dicts["mKeys"].append("guildInfo")

        #必须放在最后处理
        del_keys = ["id", "leftAt", "readAttV"]
        for del_key in del_keys:
            if del_key in dicts:
                del dicts[del_key]

            if del_key in dicts["mKeys"]:
                dicts["mKeys"].remove(del_key)

        #dicts["dailyCostContributionCount"] = self.dailyCostContributionCount
        return dicts
        
class SysGuildInfo(PlayerModifyBase):
    """
    公会记录
    """
    icon = StringField(default = "icon_1801101")
    name = StringField(default="") # 公会id
    level = IntField(default = 1) # 公会等级
    chairmanId = IntField(default="") # 会长Id
    attention = StringField(default="") # 公会公告
    attentionV = IntField(default=0) # 公会公告版本
    viChairmanIds = ListField(default = []) #副会长Id
    membersIds = ListField(default = []) # 成员idIntField(default=0)
    wood = IntField(default=0) # 公会木材
    diamond = IntField(default=0) # 公会钻石
    xp = IntField(default = 0) # 公会贡献总值
    dailyXp = IntField(default = 0) # 公会每天贡献总值
    contributeAt = DateTimeField(default=datetime.datetime.now) 
    createdInstance = IntField(default = 0) # 是解锁了副本功能
    limitLevel = IntField(default = 0) # 限制加入等级
    category = IntField(default = 1) # １随便加入，２需要审核，不允许加入
    requestMemberIds = ListField(default = []) #请求加入公会玩家ID
    outerAttention = StringField(default="") # 公会外部公告
    # TODO: 删除该字段
    siegeGuildStatus = IntField(default=-1)  # 工会战的状态
    # fireBuff =  IntField(default=0)  # 给公会成员打副本提供加成
    powerrank = IntField(default=0)  # 展示用战斗力
    fire1 = DictField(default={"buffType": 0, "buffLevel": 0, "xp": 0, "level": 1, "fireAt": 0,  "status": 1, "fireHour":0, "wood":0})#火堆1信息  status: 0未开启 1等待添加木材 2燃烧 
    fire2 = DictField(default={"buffType": 0, "buffLevel": 0, "xp": 0, "level": 0, "fireAt": 0,  "status": 0, "fireHour":0, "wood":0})#火堆2信息
    fire3 = DictField(default={"buffType": 0, "buffLevel": 0, "xp": 0, "level": 0, "fireAt": 0,  "status": 0, "fireHour":0, "wood":0})#火堆3信息
    serverid = IntField(default = 0)
    feiBookDict = DictField(default = {}) #接收到飞鸽传书的人员列表以及副本 结构为 {player_id:{str(instanceId):time.time()}}

    meta = { 
        'indexes': ["name", "-level", "serverid"],
        "shard_key": ["serverid"],
    }       

    def self_release_lock(self):
        SysGuildInfo.release_lock(self.pk)

    def save(self, *args, **kwargs):
        super(SysGuildInfo, self).save(*args, **kwargs)
        SysGuildInfo.release_lock(self.pk)

    def update(self, *args, **kwargs):
        super(SysGuildInfo, self).update(*args, **kwargs)
        SysGuildInfo.release_lock(self.pk)

    def contribute(self, xp):

        if xp > 0:
            now = datetime.datetime.now()
            if self.contributeAt.date() != now.date():
                self.dailyXp = 0

            self.xp += xp
            self.dailyXp += xp
            self.contributeAt = now

    def level_up(self, guildLevel):
        """
        升级
        """
        self.xp -= guildLevel.xp
        self.level += 1

        if self.level == 5:
            fire = self.fire2
            fire["status"] = 1
            fire["level"] = 1
            self.fire2 = fire
        elif self.level == 10:
            fire = self.fire3
            fire["status"] = 1
            fire["level"] = 1
            self.fire3 = fire
        self.save()
       

    # def memberInfo(self, id):
    #     from module.player.api import get_player
    #     player = get_player(int(id))
    #     playerGuildInfo = player.userGuild_dict()
    #     return playerGuildInfo

    def get_fire_by_index(self, index):
        """
        获取火堆信息
        """
        from guild.api import get_guildfirebuff
        if index < 1 or index > 3:
            return None

        fire = getattr(self, "fire%s" % index)

        if fire["status"] == 2:
            now = int(time.time())
            if fire["fireAt"] + fire["fireHour"] * 3600 <= now:
                firebuff = get_guildfirebuff(fire["buffType"])
                levelconf = firebuff.get_bufflevel(fire["level"], fire["buffLevel"])
                fire["xp"] += fire["fireHour"] * levelconf.woodCost
                fire["status"] = 1
                fire["fireHour"] = 0
                
                fire, _ = self.fire_checkstatus(fire)
                self.set_fire_by_index(index, fire)
                self.save()

        return fire

    def set_fire_by_index(self, index, fire):
        """
        获取火堆信息
        """
        setattr(self, "fire%s" % index, fire)

    def stop_fire_buring(self, index):
        from guild.api import get_guildfirebuff
        fire = self.get_fire_by_index(index)
        
        now = int(time.time())
        firebuff = get_guildfirebuff(fire["buffType"])
        levelconf = firebuff.get_bufflevel(fire["level"], fire["buffLevel"])
        
        seconds = now - fire["fireAt"]
        fire["xp"] += int(levelconf.woodCost * (seconds/3600.0))
        self.wood -= int(fire["wood"] * (seconds/3600.0))
        
        fire["status"] = 1
        fire["fireAt"] = 0
        fire["fireHour"] = 0
        fire["buffType"] = 0
        fire["buffLevel"] = 0
        fire["wood"] = 0
        
        self.set_fire_by_index(index, fire)
        self.save()  

    def start_fire_buring(self, index):
        now = int(time.time())
        fire = self.get_fire_by_index(index)
        fire["status"] = 2
        fire["fireAt"] = now
        
        self.set_fire_by_index(index, fire)
        self.save()     

    # def set_fire_settings(self, index, buffType, buffLevel, hour, woodCost):
    #     """
    #     更新火堆信息
    #     """
    #     from guild.api import get_guildfirebuff
    #     fire = self.get_fire_by_index(index)
    #     now = int(time.time())
        
    #     # #燃烧木头状态
    #     if fire["status"] == 2:
    #         fire["status"] = 1
    #         fire["fireHour"] = 0
    #         firebuff = get_guildfirebuff(fire["buffType"])
    #         levelconf = firebuff.get_bufflevel(fire["level"], fire["buffLevel"])
            
    #         seconds = now - fire["fireAt"]
    #         fire["xp"] += int(levelconf.woodCost * (seconds/3600.0))
    #         fire, _ = self.fire_checkstatus(fire)


    #     fire["fireAt"] = now
    #     fire["fireHour"] = hour
    #     fire["status"] = 2
    #     fire["buffType"] = buffType
    #     fire["buffLevel"] = buffLevel
    #     self.wood -= woodCost

    #     self.set_fire_by_index(index, fire)
    #     self.save()

    def set_fire_settings(self, index, buffType, buffLevel, hour, woodCost):
        """
        更新火堆信息
        """
        from guild.api import get_guildfirebuff
        fire = self.get_fire_by_index(index)
        now = int(time.time())
        
        # #燃烧木头状态
        # if fire["status"] == 2:
        #     fire["status"] = 1
        #     fire["fireHour"] = 0
        #     firebuff = get_guildfirebuff(fire["buffType"])
        #     levelconf = firebuff.get_bufflevel(fire["level"], fire["buffLevel"])
            
        #     seconds = now - fire["fireAt"]
        #     fire["xp"] += int(levelconf.woodCost * (seconds/3600.0))
        #     fire, _ = self.fire_checkstatus(fire)


        #fire["fireAt"] = now
        fire["fireHour"] = hour
        fire["status"] = 1
        fire["buffType"] = buffType
        fire["buffLevel"] = buffLevel
        #self.wood -= woodCost
        fire["wood"] = woodCost

        self.set_fire_by_index(index, fire)
        self.save()

    def fires_checkstatus(self):
        isSave = False
        for i in range(1,4):
            fire = self.get_fire_by_index(i)
            if fire["status"] == 2:
                fire, levelUp = self.fire_checkstatus(fire)
                isSave = isSave or levelUp
                if levelUp:
                    self.set_fire_by_index(index, fire)
        if isSave:
            self.save()
        else:
            SysGuildInfo.release_lock(self.pk)
    
    def fire_check(self, index):
        fire = self.get_fire_by_index(index)
        fire, levelUp = self.fire_checkstatus(fire)
        if levelUp:
            self.set_fire_by_index(index, fire)


    def fire_checkstatus(self, fire):
        """
        火堆升级
        """
        from guild.api import get_guildfirelevel
        levelup = False
        while True:
            fireLevelconf = get_guildfirelevel(fire["level"])
            next_fireLevelconf = get_guildfirelevel(fire["level"] + 1)
            if next_fireLevelconf and fire["xp"] > fireLevelconf.xp:
                fire["xp"] -= fireLevelconf.xp
                fire["level"] += 1
                levelup = True
            else:
                break

        return fire, levelup


    @property
    def viChairmanCount(self):
        return len(self.viChairmanIds)
    @property
    def membersCount(self):
        return len(self.membersIds)

    @classmethod
    def get_guild(cls, guildId, lock=True):
        """
        获取公会
        """
        if lock:
            while True:
                if cls.acquire_lock(guildId, 2):
                    break
        try:
            guild = cls.objects.get(pk=int(guildId))
        except:
            guild = None

        if lock and not guild:
            cls.release_lock(guildId)

        return guild

    @memoized_property
    def powerRank(self):
        from module.player.api import get_player
        return reduce(lambda x, y:x+y, [get_player(pk, False).powerRank for pk in self.membersIds])

    @memoized_property
    def idStr(self):
        # 这个字段是游戏里面玩家头像处那一串字符根据这个可以推算出玩家的ｉｄ
        return short_data.compress(self.pk)


    def setSiegeGuildStatus(self, siegeGuildStatus):
        self.siegeGuildStatus = siegeGuildStatus
        self.save()

    def getSiegeStatusInfo(self):
        now = datetime.datetime.now()
        year, week, day = now.isocalendar()
        hour = now.hour

        # (状态 , (周几, 几点))
        timeInfos = [(0, (1, 4)), (1, (1, 23)), (2, (2, 4)), (3, (2, 23)), (4, (6, 23)), (5, (7, 23))]
        status = 0
        endTime = 0

        for _status, _timeInfo in timeInfos:
            if day <= _timeInfo[0] and hour <= _timeInfo[1]:
                status = _status
                endTime = time.time() + (_timeInfo[0] - day) * 86400 + (_timeInfo[1] + 1 - now.hour) * 3600 - now.minute * 60 - now.second
                break

        return 3, endTime

        # if day == 1:
        #     if hour < 17:
        #         status = 0
        #     else:
        #         status = 1
        # elif day == 2:
        #     status = 1
        # elif day == 3:
        #     if hour < 8:
        #         status = 2
        #     else:
        #         status = 3
        # elif day == 4:
        #     status = 3
        # elif day == 5:
        #     status = 4
        # elif day == 6:
        #     if hour < 8:
        #         status = 4
        #     elif hour < 17:
        #         status = 5
        #     elif hour <= 23:
        #         status = 6
        # elif day == 7:
        #     status = 6


    def to_dict(self, is_all = False, is_root=False):
        dicts = super(SysGuildInfo, self).to_dict(is_all)
        from module.player.api import get_player
     
        if is_all:
            dicts["idStr"] = self.idStr

        today = datetime.datetime.now().date()
        if self.contributeAt.date() != today:
            dicts["dailyXp"] = 0

        if not is_root and (is_all or ("membersIds" in self.mKeys or "viChairmanIds" in self.mKeys or "chairmanId" in self.mKeys)):
            members = [get_player(pk, False) for pk in self.membersIds]
            dicts["powerRank"] = reduce(lambda x, y:x+y, [_player.powerRank for _player in members])
            dicts["members"] = [_player.guild.userGuild_dict(self) for _player in members]
            if len(dicts["mKeys"]) > 0:
                dicts["mKeys"].append("powerRank")
                dicts["mKeys"].append("members")
            self.powerrank = dicts["powerRank"]
            self.save()

        #必须放在最后处理
        del_keys = ["attentionV", "membersIds", "contributeAt"]
        for del_key in del_keys:
            if del_key in dicts:
                del dicts[del_key]

            if del_key in dicts["mKeys"]:
                dicts["mKeys"].remove(del_key)


        now = int(time.time())
        if "fire1" in dicts:
            if dicts["fire1"]["status"] == 2:
                dicts["fire1"]["timeLeft"] = dicts["fire1"]["fireAt"] + 3600 * dicts["fire1"]["fireHour"] + 1
            if dicts["fire1"]["status"] == 1:
                dicts["fire1"]["timeLeft"] = dicts["fire1"]["fireHour"]
                
            del dicts["fire1"]["fireAt"]
            #del dicts["fire1"]["fireHour"]

        if "fire2" in dicts:
            if dicts["fire2"]["status"] == 2:
                dicts["fire2"]["timeLeft"] = dicts["fire2"]["fireAt"] + 3600 * dicts["fire2"]["fireHour"] + 1
            if dicts["fire2"]["status"] == 1:
                dicts["fire2"]["timeLeft"] = dicts["fire2"]["fireHour"]

            del dicts["fire2"]["fireAt"]
            #del dicts["fire2"]["fireHour"]


        if "fire3" in dicts:
            if dicts["fire3"]["status"] == 2:
                dicts["fire3"]["timeLeft"] = dicts["fire3"]["fireAt"] + 3600 * dicts["fire3"]["fireHour"] + 1
            if dicts["fire3"]["status"] == 1:
                dicts["fire3"]["timeLeft"] = dicts["fire3"]["fireHour"]

            del dicts["fire3"]["fireAt"]
            #del dicts["fire3"]["fireHour"]

        dicts["siegeStatus"], dicts["siegeStatusChangeAt"] = self.getSiegeStatusInfo()
        dicts["siegeGuildStatus"] = self.siegeGuildStatus
        if len(dicts["mKeys"]) > 0:
            dicts["mKeys"].append("siegeStatus")
            dicts["mKeys"].append("siegeStatusChangeAt")
            dicts["mKeys"].append("siegeGuildStatus")

        return dicts


    def to_SimpleDict(self):
        dicts = {}
        from module.player.api import get_player
        members = [get_player(pk, False) for pk in self.membersIds]
        dicts["powerRank"] = reduce(lambda x, y:x+y, [player.powerRank for player in members])
        dicts["name"] = self.name
        dicts["level"] = self.level
        dicts["icon"] = self.icon
        dicts["limitLevel"] = self.limitLevel
        dicts["powerRank"] = self.powerrank
        dicts["outerAttention"] = self.outerAttention
        dicts["category"] = self.category
        dicts["id"] = self.pk

        chairman = get_player(self.chairmanId, False)
        dicts["members"] = [chairman.guild.userGuild_dict(chairman.guild.guildInfo)] #所有时候只需要公会会长信息
        dicts["memberCount"] = len(self.membersIds)
        dicts["requestMemberIds"] = self.requestMemberIds

        return dicts

    def change_name(self, name):
        self.name = name

    def change_icon(self, icon):
        self.icon = str(icon)

    def change_category(self, category):
        if self.category != category:
            self.requestMemberIds = []
        self.category = category
        

    def change_limitLevel(self, limitLevel):
        self.limitLevel = limitLevel

    # @property
    # def instanceIsOpen(self):
    #     return self.level >= 2


class SysGuildInstanceInfo(PlayerDataBase):
    """
    公副本记录
    """
    instanceId = IntField(default = 1) # 副本id
    guildId = IntField(default=0) # 公会id
    openStatus = IntField(default = 0) # 开启状态 0待开 1开放 2击杀 3 等待重置
    bossHp = IntField(default = 0) # boss血量
    bossPercentage = FloatField(default=0.0)
    isFighting = IntField(default=0) # 是否攻击
    fightAt = DateTimeField(default=datetime.datetime(2017,1,1))
    # 这个副本什么时候开启的
    startTime = DateTimeField(default=datetime.datetime.now)
    memberList = ListField(default = [])
    # 这个副本最后开始攻打的时间用来统计掉线超时的操作
    startFightTime = DateTimeField(default=datetime.datetime.now)
    battleStatus = DictField(default={"startCount":0, "overCount": 0}) #副本总开启次数 & 副本攻陷次数
    feiBookStatus = IntField(default=0) #本副本飞鸽传书是否发送 0 未发 1 已发

    meta = {                                                                                                                               
        'indexes': ["guildId", ("guildId", "instanceId")],
        "shard_key": ["guildId"],
    }   


    @property
    def isWaiting(self):
        return self.openStatus == 0 #等待开启

    @property
    def isOpen(self):
        return self.openStatus == 1 

    @property
    def isKill(self):
        return self.openStatus == 2 #boss被击杀

    @property
    def canFeiBook(self):
        return self.feiBookStatus == 0 #可以发飞鸽传书

    @memoized_property
    def guildInfo(self):
        if self.guildId > 0 :
            return SysGuildInfo.get_guild(self.guildId)
        return None

    def open(self):
        """
        开启
        """
        instanceLevel = get_guildinstancelevel(self.instanceId)

        self.bossHp = instanceLevel.bossHp
        self.bossPercentage = 100

        # 状态设置为开启但是没有人打
        self.openStatus = 1
        # 设置开启的时间
        self.startTime = datetime.datetime.now()
        self.memberList = []
        self.battleStatus["startCount"] += 1
        self.feiBookStatus = 0
        self.save()

    @property
    def inFighting(self):
        return self.isFighting and (datetime.datetime.now() - self.fightAt).total_seconds() < 300


    def fight(self, player):
        # 开始记录这次战斗的开始时间
        self.startFightTime = datetime.datetime.now()

        self.memberList.append(player.id)
        # 副本设置为攻打状态
        self.isFighting = 1
        self.fightAt = datetime.datetime.now()

        self.save()

    def cancel_fight(self):
        self.isFighting = 0
        self.save()

    def end_fight(self, player, bossHp, bossPercentage, isWin):
         # 更新boss的血量，boss血量不回复。
        self.bossHp = bossHp
        self.bossPercentage = bossPercentage

        if self.bossHp <= 0 and self.bossPercentage <= 0 and isWin:
            self.kill_boss()
        
        # 通知此副本并没有人正在打其他人可以打了。
        self.isFighting = 0
        self.save()

    def release_feibook_instance(self):
        sgi = self.guildInfo
        #boss被击杀时清空飞鸽传书
        _change = False
        for player_id in sgi.feiBookDict.keys():
            if str(self.instanceId) in sgi.feiBookDict[str(player_id)]:
                del sgi.feiBookDict[str(player_id)][str(self.instanceId)]
                _change = True
        if _change:
            sgi.save()


    def kill_boss(self):
        """
        击杀boss
        """
        self.killTime = datetime.datetime.now()
        self.openStatus = 2
        self.battleStatus["overCount"] += 1
        self.save()
        self.release_feibook_instance()

    @property
    def closeAt(self):
        return 24 * 60 * 60 # 秒 1天

    def check_status(self):
        """
        检查状态
        """
        # self.openStatus=0
        # self.save()
        # return

        needSave = False
        if self.isOpen or self.isKill:
            now = datetime.datetime.now()
            if (now - self.startTime ).total_seconds() >= self.closeAt:#1天自动关闭
                self.openStatus = 0 #自动关闭
                self.release_feibook_instance()
                needSave = True

            if self.isOpen:
                if self.isFighting == 1 and now - datetime.timedelta(minutes=3) > self.startFightTime.replace(tzinfo=None):
                    self.isFighting = 0
                    needSave = True

        if needSave:
            self.save()

    def get_unFighting_member_list(self):
        sgi = self.guildInfo
        #取得该公会未打过此副本的player id列表
        if sgi:
            m = list(set(sgi.membersIds) ^ set(self.memberList))
            sgi.self_release_lock()
            return m
        return []

    def get_unFighting_member_info(self):
        from player.api import get_player
        playerInfoDict = {}
        pid_list = self.get_unFighting_member_list()
        for player_id in pid_list:
            feiBook = 0 #未发飞鸽传书
            _player = get_player(player_id, lock=False)
            if str(player_id) not in playerInfoDict:
                if str(player_id) in self.guildInfo.feiBookDict:
                    feiBook = 1
                playerInfoDict[str(player_id)] = {"feiBook": feiBook, "name": _player.name, "level": _player.level, "iconId": _player.iconId}
        self.self_release_lock()
        return playerInfoDict

    def to_dict(self):
        dicts = {}
        # 副本id
        dicts["instanceId"] = self.instanceId
        # 社团id
        dicts["guildId"] = self.guildId
        # 开启状态
        dicts["openStatus"] = self.openStatus
        # boss血量
        dicts["bossHp"] = self.bossHp
        # boss百分比
        dicts["bossPercentage"] = self.bossPercentage
        # 是否有人挑战
        # startFightTime = self.startFightTime.replace(tzinfo=None)
        
        #公会内未打此副本的成员
        dicts["unMemberList"] = self.get_unFighting_member_info()

        #副本攻打状态
        dicts["battleStatus"] = self.battleStatus
        dicts["isFighting"] = self.isFighting
        # 副本开始时间
        # info["startTime"] = instance.startTime
        # 已经打过这个副本的成员
        dicts["memberList"] = self.memberList

        dicts["closeAt"] = int(datetime_to_unixtime(self.startTime + datetime.timedelta(seconds=self.closeAt))) if self.isOpen or self.isKill else 0

        return dicts

    @classmethod
    def lock_key(cls, guildId, instanceId):
        return "%s-%s" % (guildId, instanceId)

    def self_release_lock(self):
        SysGuildInstanceInfo.release_lock(self.__class__.lock_key(self.guildId, self.instanceId))

    def save(self, *args, **kwargs):
        super(SysGuildInstanceInfo, self).save(*args, **kwargs)
        SysGuildInstanceInfo.release_lock(self.__class__.lock_key(self.guildId, self.instanceId))

    def update(self, *args, **kwargs):
        super(SysGuildInstanceInfo, self).update(*args, **kwargs)
        SysGuildInstanceInfo.release_lock(self.__class__.lock_key(self.guildId, self.instanceId))


class GuildAuctionsMaxInfo(PlayerDataBase):
    """
    最大拍卖价格信息
    """
    guildId = IntField() # 公会id
    aucRewardId = IntField(default = 0)
    instanceId = IntField(default = 0)
    maxPrice = IntField(default = 0) # 当前最大值
    maxPlayerId = IntField(default = 0) # 出到最高价格的玩家
    aucStartAt = DateTimeField(default=datetime.datetime.now) # 拍卖结束的时间
    aucStatus = IntField(default = 0) # 物品的状态 0 可以出价，1已经到了一口价的价格。
    playerIds = ListField(default = [])
    prices = ListField(default = [])
    aucAts = ListField(default = [])

    meta = {                                                                                                                               
        'indexes': ["guildId", ("guildId", "aucStartAt")],
        "shard_key": ["guildId"],
    }   

    @memoized_property
    def auctionReward(self):
        from guild.api import get_guildauctionreward
        return get_guildauctionreward(self.aucRewardId)

    @property
    def aucEndAt(self):
        return self.aucStartAt.replace(tzinfo=None)  + datetime.timedelta(seconds=24*60*60)
        #return self.aucStartAt.replace(tzinfo=None)  + datetime.timedelta(1)
        
    @property
    def timeLeft(self):
        timeLeft = 0
        if self.aucStatus == 0:
            endAt = self.aucEndAt
            now = datetime.datetime.now()
            if endAt > now:
                timeLeft =  datetime_to_unixtime(endAt)

        return timeLeft

    @property
    def isAuctioning(self):
        """
        拍卖中
        """
        return  self.timeLeft > 0


    def isOffer(self, playerId):
        """
        检查player是否出价
        """
        return playerId in self.playerIds

    def auction(self,player,price):
        """
        执行拍卖
        """

        if price == self.auctionReward.maxPrice:
            self.aucStatus = 1

        if price > self.maxPrice:
            self.maxPlayerId = player.id
            self.maxPrice = price

        self.playerIds.append(player.id)
        self.prices.append(price)
        self.aucAts.append(int(time.time()))

        self.save()

    def to_dict(self):
        dicts = {}
        dicts["pk"] = self.pk
        dicts["instanceId"] = self.instanceId
        dicts["timeLeft"] = self.timeLeft
        dicts["aucRewardId"] = self.aucRewardId
        dicts["aucStatus"] = self.aucStatus
        dicts["playerIds"] = self.playerIds

        return dicts

    def self_release_lock(self):
        GuildAuctionsMaxInfo.release_lock(self.pk)

    def save(self, *args, **kwargs):
        super(GuildAuctionsMaxInfo, self).save(*args, **kwargs)
        GuildAuctionsMaxInfo.release_lock(self.pk)

    def delete(self, *args, **kwargs):
        pk = self.pk
        super(GuildAuctionsMaxInfo, self).delete(*args, **kwargs)
        GuildAuctionsMaxInfo.release_lock(pk)

class GuildLogInfo(Document):
    """
    公会日志信息
    """
    guildId = IntField() # 公会id
    logType = IntField(default = 0) # log类型
    contextParams = StringField(default="") # 主角名字填充
    logTime = DateTimeField(default=datetime.datetime.now)

    meta = {                                                                                                                               
        'indexes': ["guildId"],
        "shard_key": ["guildId"],
    }    

    def to_dict(self):
        dicts = super(guildLogInfo, self).to_dict()
        return dicts


class SysGuildSiege(Document):
    """
    工会团战信息
    """
    id = StringField(primary_key=True)#
    turn = IntField(default=0)#第几轮
    status = IntField(default=0) #0报名 1报名结果处理  2匹配阶段 

    @property
    def stage_sign_up(self):
        """
        可报名阶段
        """
        return self.status == 0

    def set_status_prematch(self):
        """
        匹配预处理
        """
        self.status = 1

    def set_status_matched(self):
        """
        匹配结束
        """
        self.status = 2

    @classmethod
    def get_opp_guildIds(cls, guildId):
        """
        获取对手工会信息
        """
         


    def get_join_guilds(self):
        """
        获取参赛工会ID
        """
        return SysGuildSiegeTurn.all(SysGuildSiege._key())

    def match_guilds(self):
        """
        第一轮匹配
        """
        guildIds = SysGuildSiege.get_join_guilds()
        random.shuffle(guildIds)
        SysGuildSiegeTurn.add(SysGuildSiege._turn_key(self.turn + 1, 1), guildIds[0::2]) #胜者组
        SysGuildSiegeTurn.add(SysGuildSiege._turn_key(self.turn + 1, 2), guildIds[1::2]) #败者组

        

    def join(self, guildId):
        """
        报名参加工会战
        """
        guildIds = self.get_join_guilds()
        if str(guildId) not in guildIds:
            SysGuildSiegeTurn.add(SysGuildSiege._key(), [guildId])

        return True

    @classmethod
    def get(cls):
        try:
            guildsiege = cls.objects.get(pk=cls._key())
        except:
            guildsiege = cls.objects.create(pk=cls._key())
        return guildsiege

    @classmethod
    def _key(cls):
        date = datetime.datetime.now().isocalendar()
        key = "Y" + str(date[0]) + "W" + str(date[1])
        return key

    @classmethod
    def _turn_key(cls, turn, winner=1):
        date = datetime.datetime.now().isocalendar()
        key = "Y" + str(date[0]) + "W" + str(date[1]) + "T" + str(turn) + "W" + str(winner)
        return key

class SysGuildSiegeTurn(StaticListRedisHandler):
    """
    工会团战每轮息人员配置
    """
    _connect_client_name = "guild"
    
# TODO: 删除该类
class GuildSiegeInfo(PlayerDataBase):
    """
    公会团战
    """
    guildIds = ListField(default="") # 报名参加的所有

    @property
    def guildNames(self):
        try:
            return [PlayerGuildInfo.objects.get(long(id)).guildName for id in self.guildIds]
        except:
            return []

    @property
    def guildPowerRanks(self):
        try:
            return [PlayerGuildInfo.objects.get(long(id)).powerRank for id in self.guildIds]
        except:
            return []


    def to_dict(self):
        info = {}
        info["guildIds"] = self.guildIds
        info["week"] = self.pk
        info["guildNames"] = self.guildNames
        info["guildPowerRanks"] = self.guildPowerRanks
        return dicts

# TODO 退出公会减去
class GuildSiegeConfigInfo(PlayerDataBase):
    """
    公会团战配置信息 
    """
    serverId = IntField(default=0)
    leftArmy = ListField(default=[{"heroInfos": [], "powerRank":0}, {"heroInfos": [], "powerRank":0}])
    middleArmy = ListField(default=[{"heroInfos": [], "powerRank":0}, {"heroInfos": [], "powerRank":0}])
    rightArmy = ListField(default=[{"heroInfos": [], "powerRank":0}, {"heroInfos": [], "powerRank":0}])
    meta = {                                                                                                                               
        "shard_key": ["serverId"],
    }

    def setLeftArmy(self, group, heroIds, power):
        if group > len(self.leftArmy):
            return False
        self.leftArmy[group]["heroInfos"] = heroIds
        self.leftArmy[group]["powerRank"] = power
        self.save()

    def setMiddleArmy(self, group, heroIds, power):
        if group > len(self.middleArmy):
            return False
        self.middleArmy[group]["heroInfos"] = heroIds
        self.middleArmy[group]["powerRank"] = power
        self.save()

    @property
    def setRightArmy(self, group, heroIds, power):
        if group > len(self.rightArmy):
            return False
        self.rightArmy[group]["heroInfos"] = heroIds
        self.rightArmy[group]["powerRank"] = power
        self.save()

    @property
    def leftPower(self):
        power = 0
        for i in range(2):
            power += self.leftArmy[i]["powerRank"]
        return power

    @property
    def middlePower(self):
        power = 0
        for i in range(2):
            power += self.middleArmy[i]["powerRank"]
        return power

    @property
    def rightPower(self):
        power = 0
        for i in range(2):
            power += self.rightArmy[i]["powerRank"]
        return power

    @property
    def allPower(self):
        power = 0
        for i in range(2):
            power += self.leftArmy[i]["powerRank"]
            power += self.middleArmy[i]["powerRank"]
            power += self.rightArmy[i]["powerRank"]
        return power

    def to_dict(self):
        dicts = super(GuildSiegeConfigInfo, self).to_dict()
        dicts["playerId"] = self.player_id
        del dicts["serverId"]
        del dicts["player_id"]
        return dicts






