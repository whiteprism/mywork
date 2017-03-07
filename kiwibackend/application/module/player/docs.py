# -*- coding: utf-8 -*-
from mongoengine import *
from module.common.docs import PlayerBase, PlayerRelationBase
import datetime
from module.common.decorators.memoized_property import memoized_property, memoized_property_delete
from module.common.decorators.save_property import save_property
from module.common.decorators.dict_property import dict_property, dict_property_get
from levelconf.api import get_level
import time
from module.common.static import Static
from task.api import get_dailytask, get_dailytasks, get_init_tasks, get_task, get_init_dailytasks, get_init_seven_days_tasks, get_seven_days_task
import datetime,threading
from vip.api import get_vip
from mail.api import has_unread_mails, send_system_mail
from loginbonus.api import get_loginbonus
from module.guild.api import get_guild
from building.models import BuildingType
import md5
from django.conf import settings

import random

from module.common.actionlog import ActionLogWriter
from module.playerplayback.api import get_army_data, get_building_army_data
from module.playerdata.api import get_playerdata
from submodule.fanyoy import short_data
from module.building.api import get_buildingproductions_by_building, get_buildingresourceprotected
#from module.guild.api import get_fireinfo_by_guildId, get_guild_by_id
from module.pvp.api import get_pvpSiegeRandomNumber
from module.offlinebonus.api import get_offlinebonuslevel, get_offlinebonusday
from module.playeritem.api import acquire_item

lockObject = threading.Lock()
def makeTime(t):
    lockObject.acquire()
    timeStamp = time.mktime(t.timetuple())
    lockObject.release()
    return timeStamp

# class PlayerModifyData(PlayerRelationBase):
#     """
#     第三方触发变更
#     碎片， 邮件
#     """
#     artifactfragments = DictField(default = {"update":[], "delete":[]})

#     def update_artifactfragment(self, obj):
#             self.artifactfragments["update"].append(obj.fragment_id)

#     def delete_artifactfragment(self, fragment_id):
#         if fragment_id not in self.artifactfragments["delete"]:
#             self.artifactfragments["delete"].append(fragment_id)

class Player(PlayerBase):
    """
    用户
    """
    name = StringField(default="")
    userid = IntField(default=0) #用户系统ID
    channel = StringField(default="")
    gold = IntField(default=0) #金币
    todayMaxGold = IntField(default=0) #今日最大金币
    yesterdayMaxGold = IntField(default=0) #之前最大金币
    yuanbo = IntField(default=0) #元宝,前端的diamond
    wood = IntField(default=0) # 木头
    todayMaxWood = IntField(default=0) #今日最大木材
    yesterdayMaxWood = IntField(default=0) #之前最大木材
    level = IntField(default=1) #等级
    iconId =  IntField(default=1140007) #萨尔
    power_dict = DictField(default = {'value':0, 'time':0})    #体力
    stamina_dict = DictField(default = {'value':0, 'time':0})  #耐力
    client_time = IntField(default=0)
    current_client_time = IntField(default=0)
    server_time = IntField(default=0)
    vip = DictField(default = {'buyRewardLevel':[], 'chargeCount':0, 'vipLevel': 0})
    xp = IntField(default=0) #经验
    couragepoint = IntField(default=0) #勇气勋章
    gashaponInfos = DictField(default={"gold":{"freeNumber":0, "last":datetime.datetime(2015,1,1)}, "yuanbo": {"last":datetime.datetime(2015,1,1)}})
    lastInstance = DictField(default = {"lastFinished":False, "lastLevelId":Static.FIRST_INSTANCE_LEVEL_ID})
    lastEliteInstance = DictField(default = {"lastEliteFinished":False, "lastEliteLevelId":0})
    starChest = ListField(default = []) #打开宝箱信息
    eliteStarChest = ListField(default = []) #打开精英宝箱信息
    heroLayout = ListField(default = []) #最后一次战斗站位信息
    defenseHeroLayout = ListField(default = []) #竞技场防守阵容站位信息
    defenseHeroIds = ListField(default=[]) #竞技场英雄防守阵容
    defenseSiegeSoldierIds = ListField(default = []) #攻城战士兵防守阵容(长度为配置点的总数，未解锁位置为-1，空的位置为0，有兵的位置为士兵ID)
    defenseSiegeLayout = ListField(default = [])#攻城战防守阵容站位信息
    defenseSiegeIds = ListField(default=[]) #攻城战英雄防守阵容
    dailyTasks = DictField(default={}) #每日任务 status 0 进行中 1已达成 2已领取
    tasks = DictField(default={}) #每日任务 status 0 进行中 1已达成 2已领取
    sevenDaystasks = DictField(default={}) #每日任务 status 0 进行中 1已达成 2已领取
    completeSevenTasks = DictField(default = {}) # 七天乐的任务完成列表
    tutorial = DictField(default={"guideGid": Static.TUTORIAL_ID_INIT_1, "status":1}) # 新手引导的记录过程
    # waravoidTime = DateTimeField(default=datetime.datetime.now) # 免战时间
    deviceId = StringField(default="")
    md5Keys = ListField(default=[])
    firstIn = IntField(default=1) #第一次进入游戏 1第一次，0,已经进入过游戏
    week_card = DictField(default={"status":0, "ended_at": None})
    month_card = DictField(default={"status":0, "ended_at": None})
    permanent_card = DictField(default={"status":0})
    loginbonus = DictField(default={"day":0, "sended_at": datetime.datetime.min}) #登陆奖励
    offlinebonus = ListField(default=[]) #离线奖励
    castleLevel =  IntField(default=0) # 主城的等级
    playerWarriorIds = ListField(default=[]) # 玩家解锁小兵信息
    endLockedTime = DateTimeField(default=datetime.datetime.now()) # 攻城战保护时间
    isOpenSiege = BooleanField(default=False) #是否开启攻城战
    isOpenArena = BooleanField(default=False) #是否开启竞技场
    halfBuyIds = ListField(default=[]) # 半价购买过的东西
    lastRaidId = IntField(default=0)
    resetRaidCount = IntField(default=0) # 100关刷新次数限制
    #pvpResetCount = IntField(default=0) # 竞技场当日刷新次数
    #pvpUpgradeScore = IntField(default=0) # 竞技场段位
    smallGameBattleCount = IntField(default=0) # 小游戏每日战斗次数

    #speedCount = IntField(default=0)
    #beSpeededCount = IntField(default=0)

    dailyTaskActivity = IntField(default=0)
    activityBoxIds = ListField(default=[])

    powerRank = IntField(default=0)
    # 爬塔币
    towerGold = IntField(default=0)
    # 活跃度
    activityValue = IntField(default=0)

    tenDiamondCount = IntField(default=0)
    isFirstTenGacha = BooleanField(default=True)
    vipDailyRewardsSendAt = DateTimeField(default=datetime.datetime(2016,1,1))
    serverid = IntField(default=settings.SERVERID)
    meta = {
        'indexes': ['level', 'name' , "endLockedTime", "isOpenSiege", "serverid"],
        'shard_key': ["serverid"],
    }
    POWER_FLUCTUATION_SECOND = Static.PLAYER_POWER_FLUCTUATION_SECOND #体力5分钟回复1点
    STAMINA_FLUCTUATION_SECOND = Static.PLAYER_STAMINA_FLUCTUATION_SECOND #耐力30分钟回复1点
    playerdata = None
    active_properties = []
    banAt = DateTimeField(default=datetime.datetime(2016,1,1)) # 封号时间
    gagAt = DateTimeField(default=datetime.datetime(2016,1,1)) # 禁言时间

    def set(self, property_name, value):
        if hasattr(self, property_name):
            if property_name not in self.active_properties:
                self.active_properties.append(property_name)

        setattr(self,property_name, value)

    def set_update(self, property_name):
        if hasattr(self, property_name):
            if property_name not in self.active_properties:
                self.active_properties.append(property_name)

    def __init__(self, **argvs):
        super(Player, self).__init__(**argvs)

        self._update_list = Player._modify_list() #更新数据
        self._delete_list = Player._modify_list() #删除数据

        self.levelup = False
        self.vip_levelup = False
        self.tutorial_change = False
        self.PVP_change = False
        self.SiegeBattle_change = False
        self.armies_change = False

        self._modify_datas = {}
        #self._playerdata_keys = []
        #self._injection_playerdata_keys = []
        self.active_properties = []

    @property
    def iDstr(self):
        # 这个字段是游戏里面玩家头像处那一串字符根据这个可以推算出玩家的ｉｄ
        return short_data.compress(self.pk)

    def get_playerdata(self, *argv):
        from module.playerdata.api import get_playerdata
        self.playerdata = get_playerdata(self, argv)

    def setBanAt(self, banAt):
        """
        设置封号时间
        """
        banAt = str(banAt)
        try:
            banAt = datetime.datetime.strptime(banAt, '%Y-%m-%d %H:%M:%S')
        except:
            return False
        self.set("banAt", banAt)
        self.update()
        return True

    def setGagAt(self, gagAt):
        """
        设置禁言时间
        """
        gagAt = str(gagAt)
        try:
            gagAt = datetime.datetime.strptime(gagAt, '%Y-%m-%d %H:%M:%S')
        except:
            return False
        self.set("gagAt", gagAt)
        self.update()
        return True

    def setPowerRank(self, powerRank):
        self.set("powerRank", powerRank)

    def setSiegeOpen(self):
        """
        开启攻城战
        """
        self.set("isOpenSiege", True)
        #初始化防守英雄站位
        defenseList = []
        default_poses = Static.HERO_DEFENCE_POS
        i = 0
        for defenseheroid in Static.SIEGE_DEFENCE_INIT[0:5]:
            defenseList.append(defenseheroid)
            defenseList.append(default_poses[i])
            i += 1
        self.defenseSiegeLayout = defenseList
        self.set_update("defenseSiegeLayout")
        #防守英雄ids
        self.set("defenseSiegeIds", Static.SIEGE_DEFENCE_INIT)
        #初始化城墙士兵
        if len(self.rampartSoldiers) > 0:
            # 删除原有的 正常情况不会有
            for soldier in self.rampartSoldiers.all().values():
                self.delete_rampartsoldier(int(soldier.pk), True)

        for soldier_id in Static.SIEGE_RAMPART_SOLDIERS:
            playersoldier = self.rampartSoldiers.create(soldierId = soldier_id, soldierLevel = 1)
            self.update_rampartsoldier(playersoldier, True)
        self.update()

    def setArenaOpen(self):
        """
        开启竞技场
        """
        self.set("isOpenArena", True)

    # def setGodessOpen(self):
    #     """
    #     开启先祖祭坛
    #     """
    #     self.set("isOpenGodess", True)

    def useFirstTenGacha(self):
        """
        标识第一次十连抽使用
        """
        self.set("isFirstTenGacha", False)

    def dailyCheck(self):
        """
        跨天数据检查
        """
        self.init_dailytasks() #每日任务初始化
        self.check_offlinebonus() #离线奖励
        self.check_loginbonus() #登陆奖励
        self.check_vipdailyrewards() #vip奖励

    def check_vipdailyrewards(self):
        """
        vip每日奖励
        """
        now = datetime.datetime.now()
        if self.vipDailyRewardsSendAt.date() < now.date():
            #同时更新玩家攻城战带币量和带木量
            self.set("yesterdayMaxGold", self.todayMaxGold)
            self.set("todayMaxGold", self.gold)
            self.set("yesterdayMaxWood", self.todayMaxWood)
            self.set("todayMaxWood", self.wood)

            vip = get_vip(self.vip["vipLevel"])
            if vip and vip.dailyRewards:
                contents = []
                contents.append({
                    "content" : "fytext_301064",
                    "paramList": [str(self.vip["vipLevel"])]
                })
                send_system_mail(player=self, sender=None, title="fytext_467", contents=contents, rewards=[reward.to_dict() for reward in vip.dailyRewards])
                self.set("vipDailyRewardsSendAt", now)

    #redis 存储
    def _get_playerdata(self, key):
        if not self.playerdata:
            self.get_playerdata()
        return getattr(self.playerdata, key)

    @property
    def activities(self):
        return self._get_playerdata("activities")

    @property
    def heroes(self):
        return self._get_playerdata("heroes")

    @property
    def armies(self):
        return self._get_playerdata("armies")

    @property
    def souls(self):
        return self._get_playerdata("souls")

    @property
    def items(self):
        return self._get_playerdata("items")

    @property
    def buildings(self):
        return self._get_playerdata("buildings")

    @property
    def buildingplants(self):
        return self._get_playerdata("buildingplants")

    @property
    def rampartSoldiers(self):
        return self._get_playerdata("rampartSoldiers")

    def get_buildings_count(self, building_id):
        return self.buildings.get_count_by_key("building_id", building_id)

    def get_plants_count(self, plant_id):
        return self.buildingplants.get_count_by_key("plantId", plant_id)

    def get_statue_count(self, building_id):
        count = 0
        if building_id in [BuildingType.STATUE_RED_LV1, BuildingType.STATUE_BLUE_LV1, BuildingType.STATUE_GREEN_LV1]:
            count += self.buildings.get_count_by_key("building_id", BuildingType.STATUE_RED_LV1)
            count += self.buildings.get_count_by_key("building_id", BuildingType.STATUE_BLUE_LV1)
            count += self.buildings.get_count_by_key("building_id", BuildingType.STATUE_GREEN_LV1)
        elif building_id in [BuildingType.STATUE_RED_LV2, BuildingType.STATUE_BLUE_LV2, BuildingType.STATUE_GREEN_LV2]:
            count += self.buildings.get_count_by_key("building_id", BuildingType.STATUE_RED_LV2)
            count += self.buildings.get_count_by_key("building_id", BuildingType.STATUE_BLUE_LV2)
            count += self.buildings.get_count_by_key("building_id", BuildingType.STATUE_GREEN_LV2)
        elif building_id in [BuildingType.STATUE_RED_LV3, BuildingType.STATUE_BLUE_LV3, BuildingType.STATUE_GREEN_LV3]:
            count += self.buildings.get_count_by_key("building_id", BuildingType.STATUE_RED_LV3)
            count += self.buildings.get_count_by_key("building_id", BuildingType.STATUE_BLUE_LV3)
            count += self.buildings.get_count_by_key("building_id", BuildingType.STATUE_GREEN_LV3)
        return count

    def get_plant_count(self):
        pass

    @property
    def equips(self):
        return self._get_playerdata("equips")

    @property
    def equipfragments(self):
        return self._get_playerdata("equipfragments")

    @property
    def artifacts(self):
        return self._get_playerdata("artifacts")

    @property
    def artifactfragments(self):
        return self._get_playerdata("artifactfragments")

    @property
    def buildingfragments(self):
        return self._get_playerdata("buildingfragments")

    @property
    def heroteams(self):
        return self._get_playerdata("heroteams")


    @property
    def gashapons(self):
        return self._get_playerdata("gashapons")

    @property
    def buyrecords(self):
        return self._get_playerdata("buyrecords")
    @property
    def buytowerrecords(self):
        return self._get_playerdata("buytowerrecords")

    @property
    def PVP(self):
        return self._get_playerdata("PVP")

    @property
    def SiegeBattle(self):
        return self._get_playerdata("SiegeBattle")

    @property
    def mysteryshop(self):
        return self._get_playerdata("mysteryshop")
    @property
    def guildshop(self):
        return self._get_playerdata("guildshop")

    @property
    def guild(self):
        return self._get_playerdata("guild")

    @property
    def guildId(self):
        guild = self.guild
        if guild:
            return guild.guildId
        return 0

    @property
    def arenashop(self):
        return self._get_playerdata("arenashop")

    @property
    def elementTower(self):
        return self._get_playerdata("elementTower")

    @property
    def yuanboshop(self):
        return self._get_playerdata("yuanboshop")

    @property
    def instancelevels(self):
        return self._get_playerdata("instancelevels")

    @property
    def eliteinstancelevels(self):
        return self._get_playerdata("eliteinstancelevels")

    @property
    def raidinstances(self):
        return self._get_playerdata("raidinstances")

    # 玩家初始化的时候会用到这个方法
    def init_md5Keys(self):
        self.md5Keys = []
        for i in xrange(1, 11):
            seed = random.randint(0, 999)
            self.md5Keys.append(seed*10 + i)

        self.set_update("md5Keys")

    def use_md5Seed(self, md5Seed):

        md5Key = md5Seed[32:37]
        md5Key = int(md5Key)
        self.md5Keys.remove(md5Key)
        if md5Key + 10 > 10000:
            self.md5Keys.append(md5Key + 10 - 10000)
        else:
            self.md5Keys.append(md5Key + 10)
        self.set_update("md5Keys")

    def check_md5(self, md5Seed):

        if len(md5Seed) != 37:
            return False

        md5Str = md5Seed[0:32]
        md5Key = md5Seed[32:37]

        md5Key = int(md5Key)
        if md5Key not in self.md5Keys:
            return False

        serverMd5Str = "%s-%s-%s" % (self.pk, md5Key, self.server_time)
        if md5.md5(serverMd5Str).hexdigest() != md5Str:
            return False
        return True

    @property
    def md5Seeds(self):
        #　选出ｋｅｙｓ里面的５个数值
        md5Keys = random.sample(self.md5Keys, 5)
        md5Seeds = []

        for md5Key in md5Keys:
            # 玩家自己的主键，挑选出来的５个值中的一个，注册服务器的时间
            md5Str = "%s-%s-%s" % (self.pk, md5Key, self.server_time)
            # 经过ｍｄ５的变换
            md5Seed = md5.md5(md5Str).hexdigest()
            md5Seed = "%s%s" % (md5Seed, str(md5Key).rjust(5,"0"))
            md5Seeds.append(md5Seed)

        return md5Seeds

    def can_buy_vip_bag(self, vip_level):
        """
        是否可以购买vip礼包
        """
        vip_level = int(vip_level)
        if self.vip["vipLevel"] < vip_level:
            return False

        if vip_level in self.vip["buyRewardLevel"]:
            return False

        return True

 #   # 为爬塔随机挑选　不同等级的buff显示在界面上，以便玩家可以进行选择
 #   def choiceBuffs(self):

  #      self.buyBuffsList = []

 #       onestars = get_buff_by_star(1)
 #       twostars = get_buff_by_star(2)
 #       threestars = get_buff_by_star(3)
 #       onebuffId = random.choice(onestars)
 #       twobuffId = random.choice(twostars)
 #       threebuffId = random.choice(threestars)
 #       self.buyBuffsList.append(onebuffId.id)
 #       self.buyBuffsList.append(twobuffId.id)
 #       self.buyBuffsList.append(threebuffId.id)

 #       self.set_update("buyBuffsList")

    def buy_vip_bag(self, vip_level):
        """
        购买vip礼包
        """
        vip_level = int(vip_level)
        self.vip["buyRewardLevel"].append(vip_level)
        self.set_update("vip")

    def add_charge_yuanbo(self, yuanbo):
        """
        添加充值金额
        """
        self.vip["chargeCount"] += yuanbo
        while True:
            vip = get_vip(self.vip["vipLevel"])
            if not vip:
                break
            if self.vip["chargeCount"] >= vip.diamond:
                next_vip = get_vip(self.vip["vipLevel"] +1)
                if next_vip:
                    self.vip["vipLevel"] += 1
                    self.vip_levelup = True
                    if str(Static.DAILYTASK_CATEGORY_VIP_SWEEP) in self.dailyTasks:
                        if self.dailyTasks[str(Static.DAILYTASK_CATEGORY_VIP_SWEEP)]["status"] == 0:
                            self.dailyTasks[str(Static.DAILYTASK_CATEGORY_VIP_SWEEP)]["status"] = 1
                            self.update_dailytask(Static.DAILYTASK_CATEGORY_VIP_SWEEP)
                            self.set_update("dailyTasks")
                else:
                    break
            else:
                break
        self.check_vipdailyrewards() #vip升级检查是否发送每日vip奖励
        self.set_update("vip")

    @property
    def vip_level(self):
        return self.vip["vipLevel"]
    @property
    def daysFromcreated(self):
        return (datetime.datetime.now().date() - self.created_at.date()).days + 1

    # # 火堆的buff
    # @property
    # def fireBuff(self):

    #     fire = get_fireinfo_by_guildId(self.guildId)
    #     if fire:
    #         fire = fire[0]
    #         if fire.timeLeft:
    #             return int(fire.fireLevel * 10000 + fire.buffType * 100 + fire.buffLevel)

    #     return 10101

    @property
    def week_card_left_day(self):
        left_days = 0
        if self.week_card["status"] == 1:
            today = datetime.date.today()
            today = datetime.datetime(today.year, today.month, today.day, 0, 0 ,0)
            left_days = (self.week_card["ended_at"]-today).days
            left_days = left_days if left_days > 0 else 0
        return left_days

    def open_week_card(self):
        today = datetime.date.today()
        if self.week_card["status"] == 0 or self.week_card["ended_at"].date() <= today:
            self.week_card["status"] = 1
            if self.check_dailytask_status(Static.DAILYTASK_CATEGORY_WEEK_CARD) == 0:
                self.dailyTasks[str(Static.DAILYTASK_CATEGORY_WEEK_CARD)]["status"] = 1
                self.update_dailytask(Static.DAILYTASK_CATEGORY_WEEK_CARD)
                self.set_update("dailyTasks")

        today = datetime.datetime(today.year, today.month, today.day, 0, 0 ,0)
        self.week_card["ended_at"] = today + datetime.timedelta(7)
        self.set_update("week_card")

    @property
    def week_card_is_activity(self):
        return self.week_card_left_day > 0

    @property
    def month_card_left_day(self):
        left_days = 0
        if self.month_card["status"] == 1:
            today = datetime.date.today()
            today = datetime.datetime(today.year, today.month, today.day, 0, 0 ,0)
            left_days = (self.month_card["ended_at"]-today).days
            left_days = left_days if left_days > 0 else 0
        return left_days

    def open_month_card(self):
        today = datetime.date.today()
        if self.month_card["status"] == 0 or self.month_card["ended_at"].date() <= today:
            self.month_card["status"] = 1
            if self.check_dailytask_status(Static.DAILYTASK_CATEGORY_MONTH_CARD) == 0:
                self.dailyTasks[str(Static.DAILYTASK_CATEGORY_MONTH_CARD)]["status"] = 1
                self.update_dailytask(Static.DAILYTASK_CATEGORY_MONTH_CARD)
                self.set_update("dailyTasks")

        today = datetime.datetime(today.year, today.month, today.day, 0, 0 ,0)
        self.month_card["ended_at"] = today + datetime.timedelta(30)
        self.set_update("month_card")

    @property
    def month_card_is_activity(self):
        return self.month_card_left_day > 0

    def open_permanent_card(self):
        if self.permanent_card["status"] == 0:
            self.permanent_card["status"] = 1
            self.set_update("permanent_card")
            if self.check_dailytask_status(Static.DAILYTASK_CATEGORY_PERMANENT_CARD) == 0:
                self.dailyTasks[str(Static.DAILYTASK_CATEGORY_PERMANENT_CARD)]["status"] = 1
                self.update_dailytask(Static.DAILYTASK_CATEGORY_PERMANENT_CARD)
                self.set_update("dailyTasks")

    @property
    def permanent_card_is_activity(self):
        return self.permanent_card["status"] == 1

    def init_dailytasks(self):
        today = datetime.date.today()
        if self.loginbonus["sended_at"].date() != today or not self.dailyTasks:
            self.dailyTasks = {}
            self.set_update("dailyTasks")
            if self.isOpenArena:
                self.PVP.reset_daily_data()

            _tasks = get_init_dailytasks()
            for _c, _t in _tasks.items():
                self.dailyTasks[str(_c)] = {"finishCount":0, "status":0, "taskGid":_t, "data":{}, "is_series":False, "is_incr":True}

                if int(_c) == Static.DAILYTASK_CATEGORY_WELFARE:
                    self.dailyTasks[str(_c)]["status"] = 1
                elif int(_c) == Static.DAILYTASK_CATEGORY_VIP_SWEEP and self.vip_level > 0:
                    self.dailyTasks[str(_c)]["status"] = 1
                elif int(_c) == Static.DAILYTASK_CATEGORY_WEEK_CARD:
                    if self.week_card_is_activity:
                        self.dailyTasks[str(_c)]["status"] = 1
                elif int(_c) == Static.DAILYTASK_CATEGORY_MONTH_CARD:
                    if self.month_card_is_activity:
                        self.dailyTasks[str(_c)]["status"] = 1
                elif int(_c) == Static.DAILYTASK_CATEGORY_PERMANENT_CARD:
                    if self.permanent_card_is_activity:
                        self.dailyTasks[str(_c)]["status"] = 1

                self.update_dailytask(_c)

    #def levelup_add_dailytasks(self):
    #    """
    #    升级添加任务
    #    """
    #    _dailytasks = get_dailytasks()
    #    for _dailytask in _dailytasks:
    #        if _dailytask.level == self.level:
    #            self.dailyTasks[str(_dailytask.pk)] = {"finishCount":0, "status":0, "taskGid":_dailytask.pk}

    def dailytask_going(self, category, number=1, c1=None, is_incr=True, is_series=False, with_top=True):
        """
        任务进行
        is_incr 自增检查  总数检查
        is_series 是否位连续的的
        with_top 只检查最大值
        """
        # is_inc 是说如果这个任务是会累计的。不论多少做一点前进一点
        # with_top 是说这个任务只关心你这次做的有没有历史最高记录好，如果有就更新成这次的值
        # is_ser是说这个任务是不是连续累计的，如果同一类型的任务接下去的任务会继承前面的完成度
        category = str(category)

        dailytasks = self.dailyTasks
        if category not in dailytasks:
            return

        dailytask = dailytasks[category]
        dailytask["is_series"] = is_series
        dailytask["is_incr"] = is_incr

        if is_incr:
            dailytask["finishCount"] += number
        else:
            if with_top:
                if dailytask["finishCount"] < number:
                    dailytask["finishCount"] = number
            else:
                dailytask["finishCount"] = number

        task = get_dailytask(dailytask["taskGid"])
        if dailytask["finishCount"] >= task.condition.count:
            if not is_series:
                dailytask["finishCount"] = task.condition.count
            dailytask["status"] = 1
        self.dailyTasks[category] = dailytask
        self.set_update("dailyTasks")
        self.update_dailytask(int(category))

    def check_dailytask_status(self, category):
        """
        检查任务是否完成
        status: 0 进行中；1，完成；2，结束
        """

        category = str(category)
        if category in self.dailyTasks:
            return self.dailyTasks[category]["status"]
        else:
            return 2

    def dailytask_is_done(self, category):
        #午餐 晚餐 夜宵
        if category in Static.DAILYTASK_MEALS_INFO:
            if str(category) in self.dailyTasks and self.dailyTasks[str(category)]["status"] == 0:
                hour = datetime.datetime.now().hour
                if Static.DAILYTASK_MEALS_INFO[category][0] <= hour < Static.DAILYTASK_MEALS_INFO[category][1]:
                    return True

        if str(category) in self.dailyTasks and self.dailyTasks[str(category)]["status"] == 1:
            task = get_dailytask(self.dailyTasks[str(category)]["taskGid"])
            if task.level > self.level:
                return False
            return True
        return False

    def dailytask_dicts(self):
        dailytasks = []
        for category, dailytask in self.dailyTasks.items():
            dailytasks.append({
                "finishCount":  dailytask["finishCount"],
                "status":  dailytask["status"],
                "taskGid":  dailytask["taskGid"],
            })
        return dailytasks

    def dailytask_dict(self, category):
        category = str(category)
        if category in self.dailyTasks:
            data = {
                "finishCount":  self.dailyTasks[category]["finishCount"],
                "status":  self.dailyTasks[category]["status"],
                "taskGid":  self.dailyTasks[category]["taskGid"],
            }
        else:
            data = {}

        return data

    def dailytask_done(self, category):
        """
        任务完成
        """
        task = get_dailytask(self.dailyTasks[str(category)]["taskGid"])
        next_task = get_dailytask(task.nextTaskId)
        if next_task:
            if  not self.dailyTasks[str(category)]["is_series"]:
                self.dailyTasks[str(category)]["finishCount"] = 0
            self.dailyTasks[str(category)]["status"] = 0
            self.dailyTasks[str(category)]["taskGid"] = next_task.pk
            if self.dailyTasks[str(category)]["is_incr"]:
                number = 0
            else:
                number = self.dailyTasks[str(category)]["finishCount"]

            self.dailytask_going(category, number=number, is_incr=self.dailyTasks[str(category)]["is_incr"], is_series=self.dailyTasks[str(category)]["is_series"])
            self.update_dailytask(category)
        else:
            del self.dailyTasks[str(category)]

        self.dailyTaskActivity += task.activityGet

        self.set_update("dailyTaskActivity")

        self.set_update("dailyTasks")

        self.delete_dailytask(task.pk)

    def task_dicts(self):
        tasks = []
        for category, task in self.tasks.items():
            tasks.append({
                "finishCount":  task["finishCount"],
                "status":  task["status"],
                "taskGid":  task["taskGid"],
            })
        return tasks

    def task_dict(self, category):
        category = str(category)
        if category in self.tasks:
            data = {
                "finishCount":  self.tasks[category]["finishCount"],
                "status":  self.tasks[category]["status"],
                "taskGid":  self.tasks[category]["taskGid"],
            }
        else:
            data = {}

        return data

    def init_tasks(self):
        self.tasks = {}
        _tasks = get_init_tasks()
        self.set_update("tasks")
        for _c, _t in _tasks.items():
            self.tasks[str(_c)] = {"finishCount":0, "status":0, "taskGid":_t, "data":{}, "is_series":False, "is_incr":True}

    def init_seven_days_tasks(self):
        self.sevenDaystasks = {}
        _tasks = get_init_seven_days_tasks()
        for _c, _t in _tasks.items():
            self.sevenDaystasks[str(_c)] = {"finishCount":0, "status":0, "taskGid":_t, "data":{}, "is_series":False, "is_incr":True}
        self.set_update("sevenDaystasks")

    def task_going(self, category, number=1, c1=None, is_incr=True, is_series=False, with_top=True):
        """
        任务进行
        is_incr 自增检查  总数检查
        is_series 是否位连续的的
        with_top 只检查最大值
        """
        category = str(category)
        if category not in self.tasks:
            return
        self.tasks[category]["is_series"] = is_series
        self.tasks[category]["is_incr"] = is_incr
        self.set_update("tasks")

        task = get_task(self.tasks[category]["taskGid"])

        # # 专门位副本关卡指定一套规则，其余任务走正常规则。
        # # c1 传入的是当前副本的id，is_incr=True, is_series=False
        if int(category) == Static.TASK_CATEGORY_INSTANCE or int(category) == Static.TASK_CATEGORY_ELIT_INSTANCE:
        #     # 只有打的那关恰好id和条件里面的数值对应才算完成一次。大于或者小于都不算
            if c1 < task.condition.c1:
                return
        # 判断任务条件是不是在当前的列表中
        if category in self.tasks:
            # 如果是增加的，就把当前完成的数量加1
            if is_incr:
                self.tasks[category]["finishCount"] += number
            else:
                # 否则如果只算总数当前完成数量小于新的数量，那就更新
                if with_top:
                    if self.tasks[category]["finishCount"] < number:
                        self.tasks[category]["finishCount"] = number
                else:
                    self.tasks[category]["finishCount"] = number
            #if int(category) == Static.TASK_CATEGORY_INSTANCE or int(category) == Static.TASK_CATEGORY_ELIT_INSTANCE:
                # if c1 == task.condition.c1:
                #     self.tasks[category]["finishCount"] = 1
            # 如果完成的数量，大于等于 条件规定的数量
            if self.tasks[category]["finishCount"] >= task.condition.count:
                # 如果不是连续的任务，那么就更新成结束时要求的数量，否则显示出来的会有问题
                if not is_series:
                    self.tasks[category]["finishCount"] = task.condition.count
                # 状态置成1，表示任务完成
                self.tasks[category]["status"] = 1

            self.update_task(int(category))

    def get_task(self, category):
        """
        获取当前任务
        """
        category = str(category)
        if category in self.tasks:
            return self.tasks[category]

        return None

    def task_is_done(self, category):
        #　如果当前的列表有这个任务并且状态为１
        category = str(category)
        if category in self.tasks and self.tasks[category]["status"] == 1:
            # 获取任务验证信息
            task = get_task(self.tasks[category]["taskGid"])
            if task.level > self.level:
                return False
            # 返回真，表示完成
            return True
        return False

    def task_done(self, category):
        """
        任务完成
        """
        category = str(category)
        # 根据类别和具体ｉｄ获取任务
        task = get_task(self.tasks[category]["taskGid"])
        # 找到任务表里面下一条的任务
        next_task = get_task(task.nextTaskId)
        c1 = None
        # 如果有下一个任务
        if next_task:
            if not self.tasks[category]["is_series"]:
                self.tasks[category]["finishCount"] = 0
            # 初始化任务状态
            self.tasks[category]["status"] = 0
            # 更新类别任务的ｉｄ，进行下一条任务
            self.tasks[category]["taskGid"] = next_task.pk
            # 如果类别是增长的，将初始数值设置为０
            if self.tasks[category]["is_incr"]:
                number = 0
            else:
                number = self.tasks[category]["finishCount"]
            if int(category) == Static.TASK_CATEGORY_INSTANCE or int(category) == Static.TASK_CATEGORY_ELIT_INSTANCE:
                if int(category) == Static.TASK_CATEGORY_INSTANCE:
                    if  self.lastInstance["lastLevelId"] > next_task.condition.c1 or (self.lastInstance["lastFinished"] and self.lastInstance["lastLevelId"] >= next_task.condition.c1):
                        self.task_going(category, number = 1, is_incr=self.tasks[category]["is_incr"],c1=next_task.condition.c1, is_series=self.tasks[category]["is_series"])
                elif int(category) == Static.TASK_CATEGORY_ELIT_INSTANCE:
                    if self.lastEliteInstance["lastEliteLevelId"] > next_task.condition.c1 or (self.lastEliteInstance["lastEliteFinished"] and self.lastEliteInstance["lastEliteLevelId"] >= next_task.condition.c1):
                        self.task_going(category, number = 1, is_incr=self.tasks[category]["is_incr"],c1=next_task.condition.c1, is_series=self.tasks[category]["is_series"])
            else:
                self.task_going(category, number = number, is_incr=self.tasks[category]["is_incr"],c1=c1, is_series=self.tasks[category]["is_series"])
            self.update_task(int(category))
        else:
            # 没有下一个任务说明所有任务完成，将这个类别的任务删除掉
            del self.tasks[category]
        self.set_update("tasks")
        self.delete_task(task.pk)

    def seven_days_task_dicts(self):
        sevenDaystasks = []
        for category, sevenDaystask in self.sevenDaystasks.items():
            sevenDaystasks.append({
                "finishCount":  sevenDaystask["finishCount"],
                "status":  sevenDaystask["status"],
                "taskGid":  sevenDaystask["taskGid"],
            })
        return sevenDaystasks

    def seven_days_task_dict(self, category):
        category = str(category)
        if category in self.sevenDaystasks:
            data = {
                "finishCount":  self.sevenDaystasks[category]["finishCount"],
                "status":  self.sevenDaystasks[category]["status"],
                "taskGid":  self.sevenDaystasks[category]["taskGid"],
            }
        else:
            data = {}

        return data

    def seven_days_task_going(self, category, number=1, c1=None, c2=None, is_incr=True, is_series=False, with_top=True):
        """
        任务进行
        is_incr 自增检查  总数检查
        is_series 是否位连续的的
        with_top 只检查最大值
        """
        category = str(category)
        if category not in self.sevenDaystasks:
            return
        self.sevenDaystasks[category]["is_series"] = is_series
        self.sevenDaystasks[category]["is_incr"] = is_incr
        self.set_update("sevenDaystasks")

        task = get_seven_days_task(self.sevenDaystasks[category]["taskGid"])
        # 判断如果建号时间小于可以做相应任务的时间，或者建号时间超过上限不做任务直接返回。
        if self.daysFromcreated >= Static.SEVEN_TASK_OVER:
            return

        # 专门位副本关卡指定一套规则，其余任务走正常规则。
        # c1 传入的是当前副本的id，is_incr=True, is_series=False
        if int(category) == Static.SEVEN_TASK_CATEGORY_INSTANCE:
            # 只有打的那关恰好id和条件里面的数值对应才算完成一次。大于或者小于都不算
            if c1 and c1 == task.condition.c1:
                pass
            else:
                return

        if int(category) in Static.SEVEN_TASK_CATEGORY_RECHARGE_LIST:
            if task.limitDay != self.daysFromcreated:
                return

        if category in self.sevenDaystasks:
            # 如果是增加的，就把当前完成的数量加1
            if is_incr:
                self.sevenDaystasks[category]["finishCount"] += number
            else:
                # 否则如果只算总数当前完成数量小于新的数量，那就更新
                if with_top:
                    if self.sevenDaystasks[category]["finishCount"] < number:
                        self.sevenDaystasks[category]["finishCount"] = number
                else:
                    self.sevenDaystasks[category]["finishCount"] = number
            # 如果完成的数量，大于等于 条件规定的数量
            if self.sevenDaystasks[category]["finishCount"] >= task.condition.count:
                # 如果不是连续的任务，那么就更新成结束时要求的数量，否则显示出来的会有问题
                if not is_series:
                    self.sevenDaystasks[category]["finishCount"] = task.condition.count
                # 状态置成1，表示任务完成
                self.sevenDaystasks[category]["status"] = 1

                # 避免类似于两次重置都完成了某个任务，会添加两次
                if str(task.pk) not in self.completeSevenTasks:
                    self.completeSevenTasks[str(task.pk)] = 0

                self.set_update("completeSevenTasks")
                self.set_update("sevenDaystasks")

            if self.seven_days_task_is_done(category):
                self.seven_days_task_done(category)

            self.update_seven_days_task(int(category))

    def get_seven_days_task(self, category):
        """
        获取当前任务
        """
        category = str(category)
        if category in self.sevenDaystasks:
            return self.sevenDaystasks[category]

        return None

    def seven_days_task_is_done(self, category):
        #　如果当前的列表有这个任务并且状态为１
        category = str(category)
        if category in self.sevenDaystasks and self.sevenDaystasks[category]["status"] == 1:
            return True
        return False

    def seven_days_task_done(self, category):
        """
        任务完成
        """
        category = str(category)
        # 根据类别和具体ｉｄ获取任务
        task = get_seven_days_task(self.sevenDaystasks[category]["taskGid"])
        # 找到任务表里面下一条的任务
        next_task = get_seven_days_task(task.nextTaskId)
        # 如果有下一个任务
        if next_task:
            if not self.sevenDaystasks[category]["is_series"]:
                self.sevenDaystasks[category]["finishCount"] = 0
            # 初始化任务状态
            self.sevenDaystasks[category]["status"] = 0
            # 更新类别任务的ｉｄ，进行下一条任务
            self.sevenDaystasks[category]["taskGid"] = next_task.pk

            # 如果类别是增长的，将初始数值设置为０
            if self.sevenDaystasks[category]["is_incr"]:
                number = 0
            else:
                number = self.sevenDaystasks[category]["finishCount"]
            if int(category) == Static.TASK_CATEGORY_INSTANCE:
                # 初始精英和普通副本的完成数量
                self.sevenDaystasks[category]["finishCount"] = 0
            self.seven_days_task_going(category, number=number, is_incr=self.sevenDaystasks[category]["is_incr"], is_series=self.sevenDaystasks[category]["is_series"])
            self.update_seven_days_task(int(category))
        else:
            # 没有下一个任务说明所有任务完成，将这个类别的任务删除掉
            del self.sevenDaystasks[category]
        self.set_update("sevenDaystasks")
        self.delete_seven_days_task(task.pk)

    # 这个当前版本，没有使用
    @property
    def populationCost(self):
        """
        使用的人口
        """
        return self.armies.population
    # 当前版本没有使用
    @property
    def population(self):
        """
        当前人口
        """
        _playerbuildings = self.buildings
        population = 0
        for _pb in _playerbuildings.all().values():
            population += _pb.population
        return population

    @property
    def power(self):
        '''
        当前体力
        '''
        self.add_power(0)
        return self.power_dict.get('value')

    def add_power(self,add_power=1):
        '''
        恢复指定体力
        '''
        add_by_time = (int(time.time()) - self.power_dict.get('time')) / Player.POWER_FLUCTUATION_SECOND
        if add_by_time < 0:
            add_by_time = 0

        if self.power_dict.get('value') >= self.levelconf.energy:
            self.power_dict['value'] = self.power_dict.get('value') + add_power
            self.power_dict['time'] = int(time.time())
        else:
            power = self.power_dict.get('value') + add_by_time
            if power >= self.levelconf.energy:
                self.power_dict['value'] = self.levelconf.energy + add_power
                self.power_dict['time'] = int(time.time())
            else:
                power += add_power
                self.power_dict['value'] = power
                if power >= self.levelconf.energy:
                    self.power_dict['time'] = int(time.time())
                else:
                    self.power_dict['time'] = self.power_dict.get('time') + add_by_time*self.POWER_FLUCTUATION_SECOND
        self.set_update("power_dict")

    @property
    def next_power_time(self):
        if self.power_dict.get('value') >= self.levelconf.energy:
            return 0
        else:
            return Player.POWER_FLUCTUATION_SECOND + self.power_dict.get('time') - int(time.time())

    def sub_power(self, delta_power=1):
        '''
        消耗指定体力
        '''
        if self.power >= delta_power and delta_power > 0:
            self.add_power(-delta_power)
            return True
        return False

    @property
    def stamina(self):
        '''
        当前体力
        '''
        self.add_stamina(0)
        return self.stamina_dict.get('value')

    def add_stamina(self,add_stamina=1):
        '''
        恢复指定体力
        '''
        add_by_time = (int(time.time()) - self.stamina_dict.get('time')) / Player.STAMINA_FLUCTUATION_SECOND
        if add_by_time < 0:
            add_by_time = 0
        if self.stamina_dict.get('value') >= self.levelconf.stamina:
            self.stamina_dict['value'] = self.stamina_dict.get('value') + add_stamina
            self.stamina_dict['time'] = int(time.time())
        else:
            stamina = self.stamina_dict.get('value') + add_by_time
            if stamina >= self.levelconf.stamina:
                self.stamina_dict['value'] = self.levelconf.stamina + add_stamina
                self.stamina_dict['time'] = int(time.time())
            else:
                stamina += add_stamina
                self.stamina_dict['value'] = stamina
                if stamina >= self.levelconf.stamina:
                    self.stamina_dict['time'] = int(time.time())
                else:
                    self.stamina_dict['time'] = self.stamina_dict.get('time') + add_by_time*self.STAMINA_FLUCTUATION_SECOND
        self.set_update("stamina_dict")

    @property
    def next_stamina_time(self):
        if self.stamina_dict.get('value') >= self.levelconf.stamina:
            return 0
        else:
            return Player.STAMINA_FLUCTUATION_SECOND + self.stamina_dict.get('time') - int(time.time())

    def sub_stamina(self, delta_stamina=1):
        '''
        消耗指定耐力
        '''
        if self.stamina >= delta_stamina and delta_stamina > 0:
            self.add_stamina(-delta_stamina)
            return True
        return False

    def  update_castlelevel(self, level):
        self.set("castleLevel", level)
        self.set_update("castleLevel")

    # checked by zy
    def get_playerbuildings_by_building_id(self, buildingid):
        # 一个玩家可能有不同级别的相同建筑.
        all_buildings = self.buildings.all().values()
        playerbuilding_list = []
        for building in all_buildings:
            if building.building_id == buildingid:
                playerbuilding_list.append(building)
        return playerbuilding_list

    @classmethod
    def _modify_list(cls):
        return {
            "heroes": [],
            "heroTeams":[],
            "souls": [],
            "buildings": [],
            "buildingFragments": [],
            "buildingPlants": [],
            "equips": [],
            "equipFragments": [],
            "items": [],
            "buyRecords": [],
            "artifacts": [],
            "artifactFragments": [],
            "activities": [],
            "mails": [],
            "battlerecords":[],
            "instancelevels": [],
            "eliteinstancelevels": [],
            "raidinstances":[],
            "dailytasks" : [],
            "tasks" : [],
            "sevenDaystasks":[],
            "rampartSoldiers":[],

        }

    @property
    def has_unread_mails(self):
        return True if has_unread_mails(self) else False

    def _update_sth(self, tag, pk):
        """
        更新
        """
        if tag not in Player._modify_list():
            return  False

        if tag not in self._modify_datas:
            self._modify_datas[tag] = {}

        if pk in self._update_list[tag]:
            return False

        self._update_list[tag].append(pk)
        return True

    def _delete_sth(self, tag, pk):
        """
        删除
        """
        if tag not in Player._modify_list():
            return  False

        if tag not in self._modify_datas:
            self._modify_datas[tag] = {}

        if pk in self._modify_datas[tag] :
            del self._modify_datas[tag][pk]

        if pk in self._update_list[tag]:
            self._update_list[tag].remove(pk)

        self._delete_list[tag].append(pk)
        return True

    def update_hero(self, playerhero, modify=False):
        if modify:
            self.heroes.update(playerhero)

        pk = playerhero.pk
        return self._update_sth("heroes", pk)

    def update_heroteam(self, playerheroteam, modify=False):
        if modify:
            self.heroteams.update(playerheroteam)

        pk = playerheroteam.pk
        return self._update_sth("heroTeams", pk)


    def update_activity(self, playeractivity, modify=False):
        if modify:
            self.activities.update(playeractivity)

        pk = playeractivity.pk
        return self._update_sth("activities", pk)

    def update_artifact(self, playerartifact, modify=False):
        if modify:
            self.artifacts.update(playerartifact)
        pk = playerartifact.pk
        return self._update_sth("artifacts", pk)

    def delete_artifact(self, pk, modify=False):
        if modify:
            self.artifacts.delete(pk)
        return self._delete_sth("artifacts", pk)

    def update_building(self, playerbuilding, modify=False):
        if modify:
            self.buildings.update(playerbuilding)
        pk = playerbuilding.pk
        return self._update_sth("buildings", pk)

    #拆除神像
    def delete_building(self, pk, modify=False):
        if modify:
            self.buildings.delete(pk)
        return self._delete_sth("buildings", pk)

    def update_buildingplant(self, playerbuildingplant, modify=False):
        if modify:
            self.buildingplants.update(playerbuildingplant)
        pk = playerbuildingplant.pk
        return self._update_sth("buildingPlants", pk)

    #铲除植物
    def delete_buildingplant(self, pk, modify=False):
        if modify:
            self.buildingplants.delete(pk)
        return self._delete_sth("buildingPlants", pk)

    def update_rampartsoldier(self, playerrampartsoldiers, modify=False):
        if modify:
            self.rampartSoldiers.update(playerrampartsoldiers)
        pk = playerrampartsoldiers.pk
        return self._update_sth("rampartSoldiers", pk)

    def delete_rampartsoldier(self, pk, modify=False):
        if modify:
            self.rampartSoldiers.delete(pk)
        return self._delete_sth("rampartSoldiers", pk)

    def update_item(self, playeritem, modify=False):
        if modify:
            self.items.update(playeritem)
        pk = playeritem.pk
        return self._update_sth("items", pk)

    def delete_item(self, pk, modify=False):
        if modify:
            self.items.delete(pk)

        return self._delete_sth("items", pk)

    def update_soul(self, playersoul, modify=False):
        if modify:
            self.souls.update(playersoul)
        pk = playersoul.pk
        return self._update_sth("souls", pk)

    def delete_soul(self, soul_id, modify=False):
        if modify:
            self.souls.delete(soul_id)
        return self._delete_sth("souls", soul_id)

    def update_buyrecord(self, playerbuyrecord, modify=False):
        if modify:
            self.buyrecords.update(playerbuyrecord)
        pk = playerbuyrecord.pk
        return self._update_sth("buyRecords", pk)

    def update_equip(self, playerequip, modify=False):
        if modify:
            self.equips.update(playerequip)
        pk = playerequip.pk
        return self._update_sth("equips", pk)

    def delete_equip(self, pk, modify=False):
        if modify:
            self.equips.delete(pk)
        return self._delete_sth("equips", pk)

    def update_equipfragment(self, playerequipfragment, modify=False):
        if modify:
            self.equipfragments.update(playerequipfragment)
        pk = playerequipfragment.pk
        return self._update_sth("equipFragments", pk)

    def delete_equipfragment(self, fragment_id, modify=False):
        if modify:
            self.equipfragments.delete(fragment_id)
        return self._delete_sth("equipFragments", fragment_id)

    def update_artifactfragment(self, playerartifactfragment, modify=False):
        if modify:
            self.artifactfragments.update(playerartifactfragment)
        pk = playerartifactfragment.pk
        return self._update_sth("artifactFragments", pk)

    def delete_artifactfragment(self, fragment_id, modify=False):
        if modify:
            self.artifactfragments.delete(fragment_id)
        return self._delete_sth("artifactFragments", fragment_id)

    def update_buildingfragment(self, playerbuildingfragment, modify=False):
        if modify:
            self.buildingfragments.update(playerbuildingfragment)
        pk = playerbuildingfragment.pk
        return self._update_sth("buildingFragments", pk)

    def delete_buildingfragment(self, fragment_id, modify=False):
        if modify:
            self.buildingfragments.delete(fragment_id)
        return self._delete_sth("buildingFragments", fragment_id)

    def update_dailytask(self, category):
        category = int(category)
        return self._update_sth("dailytasks", category)

    def delete_dailytask(self, gid):
        gid = int(gid)
        return self._delete_sth("dailytasks", gid)

    def update_task(self, category):
        category = int(category)
        return self._update_sth("tasks", category)

    def update_seven_days_task(self, category):
        category = int(category)
        return self._update_sth("sevenDaystasks", category)

    def delete_task(self, task_id):
        task_id = int(task_id)
        return self._delete_sth("tasks", task_id)

    def delete_seven_days_task(self, task_id):
        task_id = int(task_id)
        return self._delete_sth("sevenDaystasks", task_id)

    def update_mail(self, mail):
        pk = mail.pk
        return self._update_sth("mails", pk)

    def delete_mail(self, pk):
        return self._delete_sth("mails", pk)

    def update_instancelevel(self, instancelevel, modify=False):
        if modify:
            self.instancelevels.update(instancelevel)
        pk = instancelevel.pk
        return self._update_sth("instancelevels", pk)

    def update_raidinstance(self, raidinstance, modify=False):
        if modify:
            self.raidinstances.update(raidinstance)
        pk = raidinstance.pk
        return self._update_sth("raidinstances", pk)

    def update_eliteinstancelevel(self, eliteinstancelevel, modify=False):
        if modify:
            self.eliteinstancelevels.update(eliteinstancelevel)
        pk = eliteinstancelevel.pk
        return self._update_sth("eliteinstancelevels", pk)

    @property
    def gashapon_gold_free_info(self):
        now = datetime.datetime.now()
        number = 0
        left_time = 0
        if self.gashaponInfos["gold"]["last"].date() == now.date():
            number = self.gashaponInfos["gold"]["freeNumber"]
            left_time = 600-(now - self.gashaponInfos["gold"]["last"]).total_seconds()
            left_time = int(left_time) if left_time > 0 else 0

        return number, left_time

    @property
    def gashapon_yuanbo_free_info(self):
        now = datetime.datetime.now()
        number = 0
        left_time = 0
        if (now - self.gashaponInfos["yuanbo"]["last"]).days >= 2:
            number = 1
            left_time = 0
        else:
            left_time = 86400*2-(now - self.gashaponInfos["yuanbo"]["last"]).total_seconds()
            left_time = int(left_time) if left_time > 0 else 0

        return number, left_time

    @property
    def gashapon_is_gold_free(self):
        now = datetime.datetime.now()
        free = False
        if self.gashaponInfos["gold"]["last"].date() != now.date():
            free = True
        else:
            if self.gashaponInfos["gold"]["freeNumber"] < 5 and (now - self.gashaponInfos["gold"]["last"]).total_seconds() > 600 :  #当日内抽奖次数不超过5次并且两次间隔大于10分钟
                free = True
        return free

    def use_gashapon_gold_free(self):
        now = datetime.datetime.now()
        if not self.gashapon_is_gold_free:
            return False

        if self.gashaponInfos["gold"]["last"].date() != now.date():
            self.gashaponInfos["gold"]["freeNumber"] = 1
            self.gashaponInfos["gold"]["last"] = datetime.datetime.now()
        else:
            self.gashaponInfos["gold"]["freeNumber"] += 1
            self.gashaponInfos["gold"]["last"] = datetime.datetime.now()
        self.set_update("gashaponInfos")


        return True

    @property
    def gashapon_is_yuanbo_free(self):
        now = datetime.datetime.now()
        free = False
        if (now - self.gashaponInfos["yuanbo"]["last"]).days >= 2:  #每2天免费一次
            free = True
        return free

    def use_gashapon_yuanbo_free(self):
        if not self.gashapon_is_yuanbo_free:
            return False
        self.gashaponInfos["yuanbo"]["last"] = datetime.datetime.now()
        self.set_update("gashaponInfos")
        return True

    @property
    def tavern(self):
        """
        酒馆
        """
        gashapon_gold_number, gashapon_gold_left_time = self.gashapon_gold_free_info
        gashapon_yuanbo_number, gashapon_yuanbo_left_time = self.gashapon_yuanbo_free_info

        #playergashapon = self.get_gashapon(Static.GASHAPON_DIAMOND)
        tavern = {
            "dailyCustomCount": gashapon_gold_number,
            "nextGetRewardCustomTime": gashapon_gold_left_time,
            "dailyElitCount": gashapon_yuanbo_number,
            "nextGetRewardElitTime": gashapon_yuanbo_left_time,
        #    "lotteryElitCount": playergashapon.gashapon.topreward_number - playergashapon.topreward_count
        }
        return tavern

    def is_end_tutorial(self):
        return self.tutorial["guideGid"] ==  Static.TUTORIAL_ID_MAIL and self.tutorial["status"] == 2

    def end_tutorial(self):
        "结束新手向导"
        #self.tutorial_change = True
        self.tutorial["guideGid"] = Static.TUTORIAL_ID_MAIL
        self.tutorial["status"] = 2
        self.set_update("tutorial")

    def tutorial_begin(self):
        self.tutorial_change = True
        self.tutorial["guideGid"] = Static.TUTORIAL_ID_GASHAPON_2
        self.tutorial["status"] = 1
        self.set_update("tutorial")

    @property
    def tutorial_id(self):
        return self.tutorial["guideGid"]

    def next_tutorial_open(self):
        tutorial_id = self.tutorial_id
        tutorials = Static.TUTORIALS
        next_tutorial_id = tutorials[tutorials.index(tutorial_id)+1]
        self.tutorial_change = True
        self.tutorial["status"] = 1
        self.tutorial["guideGid"] = next_tutorial_id
        self.set_update("tutorial")


    def tutorial_complete(self):
        self.tutorial_change = True
        self.tutorial["status"] = 2
        self.set_update("tutorial")

    # 由于前面１０ｊ按照玩家升级去做，有顺序，但是１４ｊ以后没有顺序。
    def start_tutorial_by_id(self, tutorial_id):
        self.tutorial_change = True
        self.tutorial["guideGid"] = tutorial_id
        self.tutorial["status"] = 1
        self.set_update("tutorial")

    def add_yuanbo(self, yuanbo, info=u""):
        before_number = self.yuanbo

        self.yuanbo += yuanbo
        if self.yuanbo > 999999999:
            self.yuanbo = 999999999
        after_number = self.yuanbo

        ActionLogWriter.yuanbo_add(self, before_number, after_number, yuanbo, info)
        self.set_update("yuanbo")
        return True

    def sub_yuanbo(self, yuanbo, info=u""):
        if self.yuanbo < yuanbo:
            return False
        before_number = self.yuanbo
        self.yuanbo -= yuanbo
        after_number = self.yuanbo
        ActionLogWriter.yuanbo_cost(self, before_number, after_number, yuanbo, info)
        if self.daysFromcreated == 2:
            self.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_COST2, number=yuanbo, is_incr=True, is_series=True)
        elif self.daysFromcreated == 5:
            self.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_COST5, number=yuanbo, is_incr=True, is_series=True)
        elif self.daysFromcreated == 7:
            self.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_COST7, number=yuanbo, is_incr=True, is_series=True)

        self.set_update("yuanbo")
        return True

    def add_gold(self, gold, info=u""):
        before_number = self.gold
        self.gold += gold
        if self.gold > 999999999:
            self.gold = 999999999
        after_number = self.gold
        ActionLogWriter.gold_add(self, before_number, after_number, gold, info)

        #设置当日最大带币量
        if self.gold > self.todayMaxGold:
            self.set("todayMaxGold", self.gold)

        self.set_update("gold")
        return True

    def sub_gold(self, gold, info=u""):
        if self.gold < gold:
            return False
        before_number = self.gold
        self.gold -= gold
        after_number = self.gold
        ActionLogWriter.gold_cost(self, before_number, after_number, gold, info)
        self.set_update("gold")
        return True

    def add_wood(self, wood, info=u""):
        before_number = self.wood
        self.wood += wood
        if self.wood > 999999999:
            self.wood = 999999999
        after_number = self.wood
        ActionLogWriter.wood_add(self, before_number, after_number, wood, info)

        #设置当日最大带木量
        if self.wood > self.todayMaxWood:
            self.set("todayMaxWood", self.wood)

        self.set_update("wood")
        return True

    def sub_wood(self, wood, info=u""):
        if self.wood < wood:
            return False
        before_number = self.wood
        self.wood -= wood
        after_number = self.wood
        ActionLogWriter.wood_cost(self, before_number, after_number, wood, info)
        self.set_update("wood")
        return True


    def add_towerGold(self, count, info=u""):
        before_number = self.towerGold
        self.towerGold += count

        after_number = self.towerGold
        ActionLogWriter.tower_add(self, before_number, after_number, count, info)
        self.set_update("towerGold")
        return True

    def sub_towerGold(self, count, info=u""):
        if self.towerGold < count:
            return False
        before_number = self.towerGold
        self.towerGold -= count
        after_number = self.towerGold
        ActionLogWriter.tower_cost(self, before_number, after_number, count, info)
        self.set_update("towerGold")
        return True

    def add_couragepoint(self, couragepoint, info=u""):
        before_number = self.couragepoint
        self.couragepoint += couragepoint
        after_number = self.couragepoint
        ActionLogWriter.couragepoint_add(self, before_number, after_number, couragepoint, info)
        self.set_update("couragepoint")
        return True

    def sub_couragepoint(self, couragepoint, info=u""):
        if couragepoint <0:
            return False

        before_number = self.couragepoint
        self.couragepoint -= couragepoint
        after_number = self.couragepoint
        ActionLogWriter.couragepoint_cost(self, before_number, after_number, couragepoint, info)
        self.set_update("couragepoint")
        return True

    def sub_resetraidcount(self, count=0):
        if count < 0:
            return
        self.resetRaidCount -= count
        self.set_update("resetRaidCount")

    def layoutHeroSimple_dict(self):
        '''
        获取PVP heroes展示数据
        '''
        dicts = {}
        dicts["uid"] = self.id
        hero_list = []
        for playerhero in self.layoutHeroes:
            if playerhero:
                hero_list.append(playerhero.to_simple_dict())
        dicts["heros"] = hero_list
        return dicts

    @property
    def layoutHeroes(self):
        hero_ids = []
        for i in range(0, len(self.defenseHeroLayout), 2):
            hero_ids.append(self.defenseHeroLayout[i])

        return self.heroes.get_by_pks(hero_ids).values()

    @property
    def layoutSiegeHeroes(self):
        hero_ids = []
        for i in range(0, len(self.defenseSiegeLayout), 2):
            hero_ids.append(self.defenseSiegeLayout[i])

        return self.heroes.get_by_pks(hero_ids).values()

    def pvpSimple_dict(self, last_rank=False):
        '''
        获取PVP heroes展示数据
        '''
        dicts = {}
        dicts["uid"] = self.id
        if last_rank:
            dicts["score"] = self.PVP.lastWeekScore
            dicts["rank"] = self.PVP.lastWeekRank
        else:
            dicts["score"] = self.PVP.score
            dicts["rank"] = self.PVP.rank
        dicts["honorCount"] = Static.PVP_WIN_HONOR

        return dicts

    def userSimple_dict(self):
        '''
        获取PVP heroes展示数据
        '''
        #机器人
        robot = None
        if self.id < 0:
            from module.robot.api import get_robot
            robot = get_robot(self.id)

        dicts = {}
        dicts["icon"] =  self.iconId
        dicts["id"] = self.id
        dicts["isRobot"] = False if self.id > 0 else True
        dicts["isSetName"] = False
        dicts["lastLoginTime"] = makeTime(self.updated_at)
        dicts["level"] = self.level
        dicts["name"] = self.name
        dicts["reg_finished"] = False
        dicts["tutorial_finished"] = True
        dicts["vip"] = False if self.vip_level > 0 else True
        dicts["vipLevel"] = self.vip_level
        dicts["IDStr"] = self.iDstr
        dicts["guildName"] = self.guild.guildInfo.name if self.guildId > 0 else ""
        dicts["castleLevel"] = (robot and self.id < 0) and robot.cityLevel or self.castleLevel
        playerTowers = self.buildings.get_list_by_key("building_id", BuildingType.TOWER)
        pTowers = [t.level for t in playerTowers]
        rTowers = (robot and self.id < 0) and [robot.towerLevel for i in range(0, 2)] or []
        dicts["towerLevels"] = (robot and self.id < 0) and rTowers or pTowers
        return dicts

    def userBattleRecord_dict(self):
        '''
        获取战报展示数据
        '''
        dicts = {}
        dicts["name"] = self.name
        dicts["id"] = int(self.id)
        return dicts


    def pvp_view_data(self, can_fight=False, last_rank=False):
        '''
        给别人看得, pvp view data
        '''

        dicts = {}
        status = 0

        if can_fight:
            status = 1
        dicts["heros"] = self.layoutHeroSimple_dict()
        if last_rank:
            dicts["pvpRank"] = self.pvpSimple_dict(True)
        else:
            dicts["pvpRank"] = self.pvpSimple_dict()

        dicts["userSimple"] = self.userSimple_dict()
        dicts["status"] = status
        dicts["battlePowerRank"] = self.powerRank
        return dicts

    def siege_view_data(self ):
        '''
        给别人看得, pvp view data
        '''

        dicts = {}
        dicts["heros"] = self.layoutHeroSimple_dict()
        dicts["pvpRank"] = self.pvpSimple_dict()
        dicts["userSimple"] = self.userSimple_dict()
        dicts["status"] = 1
        dicts["battlePowerRank"] = self.powerRank
        return dicts

    @property
    def levelconf(self):
        return get_level(self.level)

    @property
    def next_levelconf(self):
        return get_level(self.level+1)

    def add_xp(self, xp):
        '''
        增加经验
        '''
        from rewards.api import reward_send

        self.xp += xp

        while self.levelconf:
            levelconf = self.levelconf
            next_levelconf = self.next_levelconf

            if self.xp >= levelconf.xp and not next_levelconf:
                self.xp = levelconf.xp
                break
            elif self.xp >= levelconf.xp and next_levelconf:
                rewards = levelconf.levelUpRewards

                for reward in rewards:
                    reward_send(self, reward, info=u"升级:%s" % (self.level+1))

                self.add_power(levelconf.rewardPower)
                self.add_stamina(levelconf.rewardStamina)
                info = u'玩家升级'
                before_level = self.level
                self.level += 1
                ActionLogWriter.player_levelup(self, before_level, self.level, xp, info)
                self.set_update("level")

                if self.level == 2 and self.tutorial_id == Static.TUTORIAL_ID_INSTANCE_1ST_3:
                    self.next_tutorial_open()
                elif self.level == 3 and self.tutorial_id == Static.TUTORIAL_ID_EQUIP_UP_4:
                    self.next_tutorial_open()
                elif self.level == 4 and self.tutorial_id == Static.TUTORIAL_ID_EQUIP_ENHANCE_6:
                    self.next_tutorial_open()

                elif self.level == 6 and self.tutorial_id == Static.TUTORIAL_ID_LOGFIELD_8:
                    self.next_tutorial_open()
                elif self.level == 7 and self.tutorial_id == Static.TUTORIAL_ID_HEROCOMPOSE2_11:
                    self.next_tutorial_open()
                elif self.level == 8 and self.tutorial_id == Static.TUTORIAL_ID_ADD_XP_12:
                    self.next_tutorial_open()
                elif self.level == 9 and self.tutorial_id == Static.TUTORIAL_ID_SKILL_LEVELUP_13:
                    self.next_tutorial_open()

                elif self.level == 10 and self.tutorial_id == Static.TUTORIAL_ID_HERO_UPGRADE_15:
                    self.check_loginbonus()
                    self.next_tutorial_open()

                # 10级　竞技场状态开启.
                #if self.level == Static.PVP_LEVEL:
                #    self.PVP._score(Static.PVP_INIT_SCORE - self.PVP.score)
                self.levelup = True
                self.xp -= levelconf.xp
                memoized_property_delete(self, "levelconf")
                self.task_going(Static.TASK_CATEGORY_LEVELUP, number=self.level, is_incr=False, is_series=True)#成长任务
            else:
                break

        self.set_update("xp")

        for category, _ in self.dailyTasks.items():
            self.update_dailytask(category)

        for category, _ in self.tasks.items():
            self.update_task(category)

        return self.levelup

    def chestWithDrawn(self, instanceId, chestLevel, isElite = False):
        '''
        记录领取的宝箱奖励
        '''
        instanceId = instanceId * 100
        if chestLevel > 2:
            chestLevel = 2
        if not isElite:
            pChest = self.starChest
        else:
            pChest = self.eliteStarChest

        if instanceId in pChest:
            index = pChest.index(instanceId)
            if not pChest[index+1] & (2 ** chestLevel):
                pChest[index+1] = pChest[index+1] | (2 ** chestLevel)
            else:
                return False
        else:
            pChest.append(instanceId)
            pChest.append((2 ** chestLevel))

        if not isElite:
            self.starChest = pChest
            self.set_update("starChest")
        else:
            self.eliteStarChest = pChest
            self.set_update("eliteStarChest")

        return True

    def update_hero_layout(self, layoutData):
        '''
        更新最新站位
        '''
        self.heroLayout = layoutData
        self.set_update("heroLayout")

    def update_hero_defenseLayout(self, layoutData):
        '''
        更新竞技场最新站位
        '''
        self.defenseHeroLayout = layoutData
        self.set_update("defenseHeroLayout")

    def update_siege_defenseLayout(self, layoutData):
        '''
        更新攻城战最新站位
        '''
        self.defenseSiegeLayout = layoutData
        self.set_update("defenseSiegeLayout")

    def update_hero_defenseHeroIds(self, defenseHeroIds):
        self.defenseHeroIds = defenseHeroIds
        self.set_update("defenseHeroIds")

    def update_siege_defenseHeroIds(self, defenseHeroIds):
        self.defenseSiegeIds = defenseHeroIds
        self.set_update("defenseSiegeIds")

    def update_siege_defenseSoldierIds(self, defenseSoldierIds):
        self.defenseSiegeSoldierIds = defenseSoldierIds
        self.set_update("defenseSiegeSoldierIds")

    def update_hero_warriorIds(self, building, buildinglevel = 1):
        buildingproductions = get_buildingproductions_by_building(building)
        key_list = []
        for buildingproduction in buildingproductions:
            if buildingproduction.buildingLevel <= buildinglevel:

                for warrior_info  in self.playerWarriorIds:
                    if warrior_info:
                        key_list.append(warrior_info["soldierId"])
                if buildingproduction.productionId not in key_list:
                        self.playerWarriorIds.append({"soldierId":buildingproduction.productionId,"soldierLevel":1})
        self.set_update("playerWarriorIds")



    def levelup_hero_warriors(self, id):
        for warrior_info in self.playerWarriorIds:

            if warrior_info["soldierId"] == int(id):
                warrior_info["soldierLevel"] += 1
                break

        self.set_update("playerWarriorIds")

    # def waravoid_add(self, delta_hour):
    #     now = datetime.datetime.now()
    #     if self.waravoidTime < now:
    #         self.waravoidTime = now
    #     self.waravoidTime += datetime.timedelta(seconds=delta_hour*3600)
    #     self.set_update("waravoidTime")

    # def reset_waravoid(self):
    #     self.waravoidTime = datetime.datetime.now()
    #     self.set_update("waravoidTime")

    # @property
    # def in_waravoid(self):
    #     now = datetime.datetime.now()
    #     return self.waravoidTime > now

    # @property
    # def waravoidCDTime(self):
    #     now = datetime.datetime.now()
    #     cd_time = (self.waravoidTime - now).total_seconds()
    #     cd_time = int(cd_time) if cd_time > 0 else 0
    #     return cd_time

    @property
    def army_data(self):
        '''
        竞技场 英雄
        '''
        return get_army_data(self)

    @property
    def building_army_data(self):
        '''
        攻城战 英雄 + 建筑 + 城墙兵
        '''
        return get_building_army_data(self)

    @property
    def wall_level(self):
        return self.levelconf.wallHp

    def check_offlinebonus(self):
        now = datetime.datetime.now()
        offlinedays = (now.date() - self.updated_at.date()).days - 1
        #离线时间小于3天或者玩家等级不足10级没有离线奖励
        # if offlinedays < 3 or self.level < 10:
        #     return
        if offlinedays > 30:
            offlinedays = 30

        offlinebonusday = get_offlinebonusday(offlinedays)
        offlinebonuslevel = get_offlinebonuslevel(self.level)
        if offlinebonusday and offlinebonuslevel:
            if offlinebonusday.rewards and offlinebonuslevel.rewards:
                rewards = offlinebonusday.rewards + offlinebonuslevel.rewards
                self.offlinebonus = []
            else:
                return
        else:
            return

        #合并天数奖励和等级奖励最初逻辑，后改为下面那种方法更简洁
        # for reward in rewards :
        #     if not self.offlinebonus:
        #         self.offlinebonus.append({
        #             "type": reward.type,
        #             "count": reward.count,
        #         })
        #     else:
        #         for data in self.offlinebonus:
        #             if reward.type == data["type"]:
        #                 data["count"] += reward.count
        #                 add = False
        #                 break
        #             else:
        #                 add = True
        #         if add:
        #             self.offlinebonus.append({
        #             "type": reward.type,
        #             "count": reward.count,
        #         })

        data = {}
        for reward in rewards:
            if reward.type not in data:
                data[reward.type] = {"type":reward.type,"count":0}
            data[reward.type]["count"] += reward.count
        self.offlinebonus = data.values()
        self.set_update("offlinebonus")

    def check_loginbonus(self):
        now = datetime.datetime.now()
        # 判断是不是同一天
        if self.loginbonus["sended_at"] and self.loginbonus["sended_at"].date() == now.date():
            return

        # 根据公会获取加速和被加速次数
        #if self.guild :#and self.guild.isActivity:
        #    guildLevel = get_guild(guild.level)
        #    self.speedCount = guildLevel.speedCount
        #    self.set_update("speedCount")
        #    self.beSpeededCount = guildLevel.beSpeededCount
        #self.set_update("beSpeededCount")

        # 竞技场刷新的次数
        #self.dailyContributionCount = 5
        #self.set_update("dailyContributionCount")
        #self.set("pvpResetCount", 1)
        self.set("smallGameBattleCount", 0)
        self.set("dailyTaskActivity", 0)
        self.set("activityBoxIds", [])

        # 每日福利
        # 如果是在七天乐的范围内，首先将今天的福利ｉｄ加入列表。
        # 如果这个人注册了账号但是隔了几天再来，那么把中间错过的几天补上，并打上过期的标志２
        # 超过９天这个活动就结束了

        if 1 <= self.daysFromcreated <= 9:
            # 手动填写ｉｄ

            if self.daysFromcreated > 7:
                end_day = 7
            else:
                completeid = 1111230 + (self.daysFromcreated - 1) * 1000010
                self.completeSevenTasks[str(completeid)] = 0
                end_day = self.daysFromcreated

            for i in range(1, end_day + 1):
                completeid = 1111230 + (i - 1) * 1000010
                if str(completeid) not in self. completeSevenTasks:
                    self.completeSevenTasks[str(completeid)] = 2

            self.set_update("completeSevenTasks")

        if (now.date() - self.loginbonus["sended_at"].date()).days > 1:
            self.loginbonus["day"] = 1
        else:
            self.loginbonus["day"] += 1
        # designed by ujy
        if self.loginbonus["day"] >= 7:
            loginbonus = get_loginbonus(7)
        else:
            loginbonus = get_loginbonus(self.loginbonus["day"])

        if loginbonus:
            rewards = []
            for reward in loginbonus.rewards:
                rewards.append({
                    "type": reward.type,
                    "count": reward.count,
                })
                # 奖励的描述是写死的。
            contents = []
            contents.append({
                "content": "fytext_300716",
                "paramList":[str(self.loginbonus["day"])]
            })
            send_system_mail(player=self, sender=None, title="fytext_300729", contents=contents, rewards=rewards)

        self.loginbonus["sended_at"] = now
        self.set_update("loginbonus")

    def self_release_lock(self):
        Player.release_lock(self.pk)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        super(Player, self).save(*args, **kwargs)

        if self.playerdata:
            self.playerdata.prepare_save()

    #第三方保存
    def passive_update(self, *args, **kwargs):
        update_values = {}
        for _property in self.active_properties:
            update_values["set__%s" % _property] = getattr(self, _property)


        if update_values:
            super(Player, self).update(**update_values)

        if self.playerdata:
            self.playerdata.prepare_save()

        Player.release_lock(self.pk)


    #自己保存
    def update(self, *args, **kwargs):

        update_values = {}
        self.set("updated_at", datetime.datetime.now())
        self.set("serverid", self.serverid)

        for _property in self.active_properties:
            update_values["set__%s" % _property] = getattr(self, _property)

        super(Player, self).update(**update_values)

        if self.playerdata:
            self.playerdata.prepare_save()

        Player.release_lock(self.pk)

    def set_lock_time(self, seconds):
        self.endLockedTime = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        self.set_update("endLockedTime")

    # @property
    # def siegeBattle_isLock(self):
    #     return self.endLockedTime > datetime.datetime.now()

    @property
    def siege_proected(self):
        percentage = 0
        if self.pk < 0:
            return percentage

        castles = self.get_playerbuildings_by_building_id(BuildingType.CASTLE)
        for caslte in castles:
            protectConf =  get_buildingresourceprotected(BuildingType.CASTLE, caslte.level)
            #gold_count += protectConf.goldCount
            #wood_count += protectConf.woodCount
            percentage += protectConf.percentage

        # 地堡 玩家可以有多个地堡
        bunker_list = self.get_playerbuildings_by_building_id(BuildingType.BUNKER)
        for bunker in bunker_list:
            protectConf =  get_buildingresourceprotected(BuildingType.BUNKER, bunker.level)
            #gold_count += protectConf.goldCount
            #wood_count += protectConf.woodCount
            percentage += protectConf.percentage

        return percentage

    def calculate_siege_spoilrewards(self):
        # 这是计算玩家攻城战可以被抢夺多少资源。
        now = datetime.datetime.now()
        result = []
        #randint = random.randint(1, 1000)
        if self.id < 0:
            randint = random.randint(1, 266)
            pvpSiegeRandomNumber = get_pvpSiegeRandomNumber(randint)
            gold_result = int(self.level * pvpSiegeRandomNumber.number * 300 + randint)
            wood_result = int(self.level * pvpSiegeRandomNumber.number * 100 + randint)
        else:
            percentage = self.siege_proected
            gold_count = self.yesterdayMaxGold if self.yesterdayMaxGold > 0 else self.todayMaxGold
            gold_result = int(gold_count * (1 - percentage))
            wood_count = self.yesterdayMaxWood if self.yesterdayMaxWood > 0 else self.todayMaxWood
            wood_result = int(wood_count * (1 - percentage))


        max_gold = (-10/(0.2 * self.level + 1.5) +3 ) * 100000
        max_wood = (-10/(0.2 * self.level + 1.5) +3 ) * 30000

        gold_result = gold_result if gold_result <= max_gold else max_gold
        wood_result = wood_result if wood_result <= max_wood else max_wood

        gold_result = int(gold_result)
        wood_result = int(wood_result)

        result = {"wood":wood_result , "gold": gold_result}
        return result

    def lost_siegebattle_result(self, gold, wood):
        info = u"攻城战失利"
        self.sub_gold(gold, info=info)
        self.sub_wood(wood, info=info)

    def win_siegebattle_result(self, gold, wood):
        info = u"攻城战胜利"
        self.add_gold(gold, info=info)
        self.add_wood(wood, info=info)

    @property
    def smallGameLeftTimes(self):
        """
        小游戏每日剩余战斗次数
        """
        return 3 - self.smallGameBattleCount if 3 - self.smallGameBattleCount > 0 else 0

    def smallGameBattle(self):
        self.set("smallGameBattleCount", self.smallGameBattleCount + 1)

    @property
    def is_onLine(self):
        now = datetime.datetime.now()
        return (now - self.updated_at).total_seconds() < 5#1200
