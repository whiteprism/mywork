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

    INIT_BATTLE_TIMES = 100 #每日默认战斗次数
    battleTimes = IntField(default = 0)  #每日战斗
    winCount = IntField(default = 0) #累計戰勝次數
    cd_time = DateTimeField(default=datetime.datetime.min) #战斗失败冷却时间
    opps = ListField(default=[]) #对手信息 {“playerId”:xx, "wood":xx, "gold": xx, "isLocked":xxx}
    pkOpp = DictField(default={}) #正在战斗对手
    forts = ListField(default=[0,0,0,0,0])#5个运输堡垒
    autoRefreshAt = DateTimeField(default=datetime.datetime.now)
    REFRESH_HOURS = [23, 11, 0]

    def load(self, player):
        super(self.__class__, self).load(player)
        today = datetime.date.today()
        if self.updated_at.date() < today:
            self.battleTimes = 0

    def get_opp(self, oppId):
        for opp in self.opps:
            if opp["player_id"] == oppId:
                return opp
        return None

    def set_pkOpp(self, opp):
        self.pkOpp = opp
        self.update()

    @property
    def oppsLockCount(self):
        count = 0
        for opp in self.opps:
            if opp["isLocked"]:
                count += 1
        return count

    @classmethod
    def _before_refresh_hour(cls, hour):
        for _h in cls.REFRESH_HOURS:
            if _h < hour:
                return _h
        return _h

    @classmethod
    def _next_refesh_hour(cls, hour):
        before_hour = cls._before_refresh_hour(hour)
        _index = cls.REFRESH_HOURS.index(before_hour)
        return cls.REFRESH_HOURS[_index-1]

    @property
    def leftRefreshTime(self):
        """
        剩余自动刷新时间
        """
        now = datetime.datetime.now()
        next_refesh_hour = PlayerSiegeBattle._next_refesh_hour(now.hour)
        end_time = datetime.datetime(now.year, now.month, now.day, next_refesh_hour, 59, 59)
        return ( end_time - now ).total_seconds() + 4

    def refresh_auto(self, force=False):
        now = datetime.datetime.now()
        if not force and self.autoRefreshAt.date() == now.date():
            if PlayerSiegeBattle._before_refresh_hour(self.autoRefreshAt.hour)  ==  PlayerSiegeBattle._before_refresh_hour(now.hour) :
                return False
        self.autoRefreshAt = now
        self.refresh()
        return True

    def refresh(self, replaceOppId=0):
       from module.player.api import refresh_siegebattle_players
       self.opps = refresh_siegebattle_players(self.player, replaceOppId)
       self.update()

    def replaceOpp(self):
        opp = self.pkOpp
        self.refresh(opp["player_id"])

    @property
    def fortInfos(self):
        now = int(time.time())
        forts = []
        for fort in self.forts:
            if fort > 0 and fort < now:
                fort = 0
            forts.append(fort)

        return forts

    def fort_canReset(self, index):
        fortInfos = self.fortInfos

        if index > len(fortInfos) or index < 1:
            return False
        return fortInfos[index - 1] > 0

    def forts_reset(self, fortIndexes):
        for fortIndex in fortIndexes:
            self.forts[fortIndex - 1] = 0
        self.update()

    def forts_use(self, fortIndexes):
        for fortIndex in fortIndexes:
            self.forts[fortIndex - 1] = (time.time()) + Static.SIEGE_FORT_CD_TIME
        self.update()

    def to_dict(self):
        from module.player.api import get_player
        dicts = {}
        leftTimes = self.INIT_BATTLE_TIMES - self.battleTimes
        dicts["leftTimes"] = leftTimes if leftTimes > 0 else 0
        dicts["cdTime"] = self.cdTime #冷却时间
        dicts["forts"] = self.fortInfos
        opps = []
        if not self.opps:
            self.refresh_auto(True)

        for _opp in self.opps:
            _player = get_player(_opp["player_id"], False)
            siegeViewData = _player.siege_view_data()
            siegeViewData["grabRewards"] = _opp["rewards"]
            siegeViewData["isLocked"] = _opp["isLocked"]
            opps.append(siegeViewData)
        dicts["opps"] = opps

        return dicts

    def add_winCount(self, add_count=1):
        '''
        战胜的总次数
        '''

        self.winCount += add_count

    def use_battleTimes(self):
        self.battleTimes += 1

    @property
    def canBattle(self):
        leftTimes = self.INIT_BATTLE_TIMES - self.battleTimes
        return leftTimes > 0

    @property
    def cdTime(self):
        '''
        冷却剩余时间
        '''
        if self.cd_time.replace(tzinfo=None) > datetime.datetime.now():
            return datetime_to_unixtime(self.cd_time)
        return 0

    def reset_cdTime(self):
        self.cd_time = datetime.datetime.now()

    def set_cdTime(self):
        self.cd_time = datetime.datetime.now() + datetime.timedelta(seconds=Static.SIEGE_PVP_CD_TIME)

    @property
    def isInCDTime(self):
        return self.cdTime > 0
