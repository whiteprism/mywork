# -*- coding: utf-8 -*-
from mongoengine import *
from common.docs import PlayerRelationBase, PlayerRedisDataBase, PlayerBase
import datetime, math, time
from module.utils import delta_time, datetime_to_unixtime
from module.common.static import Static
from submodule.fanyoy.redis import StaticSortedSetDataRedisHandler, StaticSingleDataRedisHandler
from module.common.actionlog import ActionLogWriter
from module.pvp.api import get_pvpUpgradeScore, get_pvpUpgradeScoreKeys
from module.mail.api import send_system_mail
from vip.api import get_vip
import random
import cPickle
from django.conf import settings

class PlayerPVPYesterdayData(StaticSingleDataRedisHandler):
    """
    玩家PVP昨日数据
    """
    @classmethod
    def get_data(cls):
        dataStr = cls.get(settings.SERVERID)
        if dataStr:
            data = cPickle.loads(dataStr)
        else:
            data = []
        return data

    @classmethod
    def set_data(cls, data):
        dataStr = cPickle.dumps(data)
        cls.set(dataStr, settings.SERVERID)

class PlayerPVPLastWeekData(StaticSingleDataRedisHandler):
    """
    玩家PVP上周数据
    """
    @classmethod
    def get_data(cls):
        dataStr = cls.get(settings.SERVERID)
        if dataStr:
            data = cPickle.loads(dataStr)
        else:
            data = []
        return data

    @classmethod
    def set_data(cls, data):
        dataStr = cPickle.dumps(data)
        cls.set(dataStr, settings.SERVERID)

class PVPRank(StaticSortedSetDataRedisHandler):
    """
    pvp排行
    """
    #有调用父类方法时，默认key一定要赋值为本类中_key()方法的返回值

    @classmethod
    def rankLenth(cls):
        """
        获得长度
        return int
        Return the number of elements in the sorted set name
        """
        return cls.length(key=cls._key())

    @classmethod
    def _key(cls):
        date = datetime.datetime.now().isocalendar()
        key = "S" + str(settings.SERVERID) + "Y" + str(date[0]) + "W" + str(date[1])
        return key

    @classmethod
    def _yesterday_key(cls):
        date = (datetime.datetime.now() - datetime.timedelta(1)).isocalendar()
        key = "S" + str(settings.SERVERID) + "Y" + str(date[0]) + "W" + str(date[1])
        return key

    @classmethod
    def _key_by_week(cls, year, week):
        key = "S" + str(settings.SERVERID) + "Y" + str(year) + "W" + str(week)
        return key

    @classmethod
    def _last_week_key(cls):
        date = (datetime.datetime.now() - datetime.timedelta(7)).isocalendar()
        key = "S" + str(settings.SERVERID) + "Y" + str(date[0]) + "W" + str(date[1])
        return key

    @classmethod
    def get_ranks(cls):
        all_rank = PVPRank.range(0, 99, key=PVPRank._key())
        yoyprint(u"0 到100 的排名")
        return all_rank

    @classmethod
    def get_yesterday_ranks(cls, start=0, end=99):
        all_rank = PVPRank.range(start, end, key=PVPRank._yesterday_key())
        yoyprint(u"0 到100 的排名")
        return all_rank

    @classmethod
    def get_last_ranks(cls, start=0, end=99):
        all_rank = PVPRank.range(start, end, key=PVPRank._last_week_key())
        #yoyprint(u"0 到100 的上周排名")
        return all_rank

    @classmethod
    def get_last_ranks_by_score(cls, min_score, max_score):
        '''
        返回范围排名的rank list
        '''
        return PVPRank.rangebyscore(min_score, max_score, key=PVPRank._last_week_key())

    @classmethod
    def range_by_rank(cls, start, end):
        '''
        根据排名获取排名
        '''
        return cls.range(start, end, key=PVPRank._key())

    @classmethod
    def range_by_score(cls, min_score, max_score):
        '''
        返回范围排名的rank list
        '''
        return PVPRank.rangebyscore(min_score, max_score, key=PVPRank._key())

    @classmethod
    def result_score(cls, player_score, target_player_score, isWin):
        '''
        结算积分
        '''
        k = Static.PVP_SCORE_K
        Rn = k*(int(isWin) - cls.win_expectation(player_score, target_player_score))
        return int(math.ceil(Rn))

    @classmethod
    def win_expectation(cls, player_score, target_player_score):
        '''
        玩家对对手的期望胜率
        '''
        if target_player_score - player_score > 735:
            return 0.1
        EA = 1.0 / (1 + 10 ** (-(player_score - target_player_score) / 200.0))
        return round(EA, 3)

    @classmethod
    def diff_value(cls, win_expectation):
        '''
        根据期望获取差值
        '''
        return int(round(400*math.log10(1/win_expectation-1)))

class PlayerPVP(PlayerRedisDataBase):
    '''
    用户pvp
    '''
    attackNum = IntField(default = 0)
    defenceNum = IntField(default = 0)
    surplusCount = IntField(default = 0)
    honor = IntField(default = 0) #荣誉点数
    serieWins = IntField(default = 0) #连胜
    keepSerieWinCount = IntField(default = 0) #花钱刷新列表次数 跟着每日任务的刷新时间走（清零）
    serieWin_time = DateTimeField(default=datetime.datetime.min) #连胜开始时间
    cd_time = DateTimeField(default=datetime.datetime.min) #打完一场时间
    freeBattleCount = IntField(default = 5)
    battleRecord = ListField(default = []) # 战报记录
    dailyRank = IntField(default = 0)
    resetCount = IntField(default = 0) #每日重置次数
    upgradeScore = IntField(default = 0) #段位积分
    upgradeScoreWeek = StringField(default = PVPRank._key) #段位积分

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["rank"] = self.rank
        dicts["serieWinLeftTime"] = self.winTime
        dicts["honor"] = self.honor
        dicts["point"] = self.score
        dicts["serieWins"] = self.serieWins
        dicts["cdTime"] = self.cdTime
        dicts["resetCost"] = self.resetCost

        del dicts["id"]
        del dicts["serieWin_time"]
        del dicts["cd_time"]
        return dicts

    def reset_daily_data(self):
        self.keepSerieWinCount = 0
        self.resetCount = 0
        self.freeBattleCount = 5
        weekKeys = PVPRank._key()
        if self.upgradeScoreWeek != weekKeys:
            self.upgradeScoreWeek = weekKeys
            self.upgradeScore = 0
        self.update()

    @property
    def resetCost(self):
        diamond = 0
        diamond = 50 * (self.resetCount + 1)
        return diamond if diamond <= 200 else 200

    def add_honor(self, honor, info=u""):
        before_number = self.honor
        self.honor += honor
        after_number = self.honor
        ActionLogWriter.honor_add(self.player, before_number, after_number, honor, info)
        self.update()
        return True

    def sub_honor(self, honor, info=u""):
        if self.honor < honor:
            return False
        before_number = self.honor
        self.honor -= honor
        after_number = self.honor
        ActionLogWriter.honor_cost(self.player, before_number, after_number, honor, info)
        self.update()
        return True

    def subBattleCount(self):
        self.freeBattleCount -= 1
        if self.freeBattleCount <= 0:
            self.freeBattleCount = 0
        self.update()

    def resetPVPCount(self):
        self.freeBattleCount = 5
        self.resetCount += 1
        self.update()

    def get_oppIds(self):
        """
        获取对战列表的人
        """

        return self.update_oppIds()

    def update_oppIds(self):
        """
        更新PVP列表, 获取当前最新的人
        """
        opponent_ids = []

        rank = self.rank

        if rank - 20 >= 0:
            start = rank - 20
        else:
            start = 0

        end = rank + 19
        result = PVPRank.range_by_rank(start, end)
        for id, score in result:
            if int(id) != self.player.id:
                opponent_ids.append(id)

        return opponent_ids

    @property
    def winTime(self):
        '''
        连胜剩余时间
        '''
        if self.serieWins:
            over_time = delta_time(self.serieWin_time)
            if over_time > Static.UPDATE_TIME_SERIE_WIN:
                self.serieWins = 0
                self.update()
            else:
                return Static.UPDATE_TIME_SERIE_WIN - over_time
        return 0

    @property
    def cdTime(self):
        '''
        冷却剩余时间
        '''

        if self.cd_time.replace(tzinfo=None) > datetime.datetime.now():
            return datetime_to_unixtime(self.cd_time)
        return 0


    def updateCdTime(self):
        self.cd_time = datetime.datetime.now() + datetime.timedelta(seconds=Static.PVP_CD_TIME)
        return self.cd_time

    def update_serie_win(self):
        '''
        更新serie win
        '''
        if not self.winTime:
            self.serieWins = 0
            self.update()

        return self.serieWins

    @property
    def score(self):
        '''
        积分
        '''
        if self.player.pk > 0:
            init_default = self.player.isOpenArena
        else:
            init_default = False

        print self.player.pk, init_default, "init score"
        
        return PVPRank.score(self.player.pk, key=PVPRank._key(), default=Static.PVP_INIT_SCORE, init_default=init_default)


    @property
    def rank(self):
        '''
        排名
        '''
        return PVPRank.rank(self.player.pk, key=PVPRank._key())

    @property
    def yesterdayScore(self):
        '''
        排名
        '''
        return PVPRank.score(self.player.pk, key=PVPRank._yesterday_key())


    @property
    def yesterdayRank(self):
        '''
        排名
        '''
        return PVPRank.rank(self.player.pk, key=PVPRank._yesterday_key())

    @property
    def yesterdarankandscore(self):
        """
        return rank, score
        """
        return PVPRank.rankandscore(self.player.pk, key=PVPRank._key())

    def score_by_week(self, year, week):
        '''
        积分
        '''
        return PVPRank.score(self.player.pk, key=PVPRank._key_by_week(year, week))

    def rank_by_week(self, year, week):
        '''
        排名
        '''
        return PVPRank.rank(self.player.pk, key=PVPRank._key_by_week(year, week))

    @property
    def lastWeekScore(self):
        '''
        上周积分
        '''
        return PVPRank.score(self.player.pk, key=PVPRank._last_week_key())

    @property
    def lastWeekRank(self):
        '''
        上周排名
        '''
        return PVPRank.rank(self.player.pk, key=PVPRank._last_week_key())

    def add_score(self, score):
        '''
        增加积分
        '''
        if score < 0:
            if -score > self.score:
                score = -self.score
        new_score = PVPRank.incrby(self.player.pk, score, key=PVPRank._key())
        return new_score

    def set_score(self, score):
        '''
        设置积分
        '''
        PVPRank.add({self.player.pk:score}, key=PVPRank._key())

    def rankandscore(self):
        """
        return rank, score
        """
        return PVPRank.rankandscore(self.player.pk, key=PVPRank._key())

    def win(self, target_player):
        '''
        PVP胜利调用
        '''

        result_score = int(32 * (1-(1/(1 + math.pow(10, (-(self.score - target_player.PVP.score)/250))))))
        self.add_score(result_score)

        result, upScore = self.checkUpgrade()

        if result:
            upScoreInfo = get_pvpUpgradeScore(upScore)

            rewards = []
            for reward in upScoreInfo.rewards:
                rewards.append(reward.to_dict())

            contents = []
            contents.append({
                "content": upScoreInfo.mulLang,
                "paramList": [str(upScore), str(upScoreInfo.upgrade)],
            })

            send_system_mail(player=self.player, sender=None, title="fytext_300725", contents=contents, rewards=rewards)
            

        return result_score
    def lose(self, target_player_score):
        '''
        PVP 失败
        '''
        #print "失败双方积分位：", self.score, target_player_score
        # self.serieWins = 0
        # result_score = PVPRank.result_score(self.score, target_player_score, False)
        #print "PVP 失败扣除积分为:", result_score
        result_score = -int(32 * (1-(1/(1 + math.pow(10, ((self.score - target_player_score)/250))))))
        self.add_score(result_score)
        return result_score


    def checkUpgrade(self):
        res = False
        upScore = 0
        scoreKeys = get_pvpUpgradeScoreKeys()
        for score in scoreKeys:
            if self.score >= score and score > self.upgradeScore:
                self.upgradeScore = score
                self.update()
                res = True
                upScore = score
                break
            elif self.score < score:
                continue
            else:
                break
        return res, upScore


class PlayerSiegeBattle(PlayerRedisDataBase):
    """
    攻城战
    """
    forts = ListField(default=[]) # 堡垒的冷却时间 元素个数为堡垒总数 vip升级数量有变
    resources = ListField(default=[]) # [{"wood":xxx, "gold": xxx, "arrivalTime": time.time},] 元素个数为车辆总数
    oppId = IntField(default = 0) # 对手id
    lastBattleResult = BooleanField(default=False) # 上次对战结果
    resourcesCount = IntField(default = 0) # 能被掠夺的车辆数量 

    def init_forts(self):
        vip = get_vip(self.player.vip_level)
        t = time.time()
        if len(self.forts) == vip.fortCount:
            return
        for i in range(0, vip.fortCount-len(self.forts)):
            self.forts.append(t)
        self.update()

    def add_forts(self, count):
        t = time.time()
        for i in range(count):
            self.forts.append(t)
        self.update()

    def searchOpp(self):
        """
            搜索对手
        """
        from module.player.api import search_siegebattle_player
        opp = search_siegebattle_player(self.player)
        self.oppId = opp.id
        self.update()
        if opp.id > 0:
            opp.siege_be_searched() # 设置被匹配的保护时间
        return opp

    def fightEnd(self, isWin):
        """
            结束战斗
        """
        self.lastBattleResult = isWin
        self.update()

    @property
    def has_fort(self):
        """
            有未使用的堡垒
        """
        now = time.time()
        for _time in self.forts:
            if _time < now:
                return True
        return False

    def use_fort(self):
        """
            使用堡垒
        """
        vip = get_vip(self.player.vip_level)
        now = time.time()
        for _i,_time in enumerate(self.forts):
            if _time < now:
                self.forts[_i] = now + vip.fortTime
                print _time
                break
        self.update()

    def can_reset_fort(self, index):
        now = time.time()
        if index >= len(self.forts):
            return False
        return self.forts[index] > now

    def reset_fort(self, index):
        if index >= len(self.forts):
            return
        self.forts[index] = 0
        self.update()

    @property
    def reset_fort_cost(self):
        """
            消除一个堡垒的消耗
        """
        vip = get_vip(self.player.vip_level)
        return vip.resetCost

    @property
    def has_truck(self):
        """
            车辆未达上限
        """
        vip = get_vip(self.player.vip_level)
        return len(self.resources) < vip.transitCount

    def get_resources(self):
        """
            搜索 可被掠夺的资源
        """
        resource = {
            "wood": 0,
            "gold": 0,
            "arrivalTime": 0
        }
        bunker_protect = self.player.siege_bunker_protected # 地保保护量
        caslte_percent = self.player.siege_caslte_protected # 主城保护百分比
        self.resourcesCount = 0
        for item in self.resources:
            if item["arrivalTime"] - time.time() > 240:
                # 大于四分钟的资源才可被掠夺
                self.resourcesCount += 1
                wood = (item["wood"] > bunker_protect["wood"] and (item["wood"] - bunker_protect["wood"]) or item["wood"]) * (1 - caslte_percent)
                gold = (item["gold"] > bunker_protect["gold"] and (item["gold"] - bunker_protect["gold"]) or item["gold"]) * (1 - caslte_percent)
                resource["wood"] += wood
                resource["gold"] += gold
        self.update()
        return resource

    def get_resources_settlement(self):
        """
            结算 可被掠夺的资源
        """
        resource = {
            "wood": 0,
            "gold": 0,
            "arrivalTime": 0
        }
        bunker_protect = self.player.siege_bunker_protected # 地保保护量
        caslte_percent = self.player.siege_caslte_protected # 主城保护百分比
        length = len(self.resources)
        for i in range(self.resourcesCount):
            item = self.resources[length - i - 1]
            wood = (item["wood"] > bunker_protect["wood"] and (item["wood"] - bunker_protect["wood"]) or item["wood"]) * (1 - caslte_percent)
            gold = (item["gold"] > bunker_protect["gold"] and (item["gold"] - bunker_protect["gold"]) or item["gold"]) * (1 - caslte_percent)
            self.resources[length - i - 1]["wood"] -= wood
            self.resources[length - i - 1]["gold"] -= gold
            resource["wood"] += wood
            resource["gold"] += gold
        self.update()
        return resource

    def from_resource_to_reward(self, resource):
        """
            将resource 封装成 reward
        """
        from rewards.models import CommonReward
        rewards = []
        try:
            rewardGold = CommonReward(type=50000, count=resource["gold"], level=0)
            rewardWood = CommonReward(type=60000, count=resource["wood"], level=0)
            rewards.append(rewardGold)
            rewards.append(rewardWood)
        except:
            return rewards
        return rewards

    def add_resource(self, resource):
        """
            添加资源到运输列表中
        """
        vip = get_vip(self.player.vip_level)
        if resource.has_key("wood") and resource.has_key("gold") and resource.has_key("arrivalTime"):
            resource["arrivalTime"] = time.time() + vip.transitTime
            self.resources.append(resource)
            self.update()
            # if not self.player.hasResource:
            #     # 如果没有标记自己有未到达的资源，则标记
            #     self.player.set_hasresource(True)
        return self.resources

    # def sub_resource(self):
    #     """
    #         资源被掠夺
    #     """
    #     vip = get_vip(self.player.vip_level)
    #     bunker_protect = self.player.siege_bunker_protected # 地保保护量
    #     caslte_percent = self.player.siege_caslte_protected # 主城保护百分比
    #     for item in self.resources:
    #         wood = (item["wood"] > bunker_protect["wood"] and (item["wood"] - bunker_protect["wood"]) or item["wood"]) * (1 - caslte_percent)
    #         gold = (item["gold"] > bunker_protect["gold"] and (item["gold"] - bunker_protect["gold"]) or item["gold"]) * (1 - caslte_percent)
    #         item["wood"] -= wood
    #         item["gold"] -= gold
    #     self.update()

    def check_resource(self, index):
        """
            检查是否有资源到达
        """ 
        info = u"攻城战资源到达"
        now = time.time()
        if index >= len(self.resources):
            return False
        if self.resources[index]["arrivalTime"] <= now:
            self.player.add_gold(self.resources[index]["gold"], info = info)
            self.player.add_wood(self.resources[index]["wood"], info = info)
            self.resources.pop(index)
        # if len(self.resources) == 0:
        #     # 没有正在运输的资源
        #     self.player.set_hasresource(False)
        self.update()
        return True

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        del dicts["lastBattleResult"]
        del dicts["resourcesCount"]
        return dicts

