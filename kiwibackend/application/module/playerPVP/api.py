# -*- coding: utf-8 -*-
from module.common.static import Static
import random
import datetime
from module.artifact.api import get_artifactfragment
from module.playerartifact.api import acquire_artifactfragment
from module.pvp.api import get_pvpRanks
from module.common.static import Static
from module.mail.api import send_system_mail
from player.api import get_all_player, get_player
from module.player.docs import Player
from module.playerPVP.docs import PVPRank,PlayerPVPYesterdayData, PlayerPVPLastWeekData

from module.robot.api import get_robot


def get_lastweek_rank(limit=100):
    data = PlayerPVPLastWeekData.get_data()
    return data[0:100]

def get_yesterday_rank(limit=100):
    data = PlayerPVPYesterdayData.get_data()
    return data[0:100]

def pvp_fight(player, target_player, isWin, fragmentId=0):
    '''
    PVP 结算
    '''
    rewards = []
    golds = Static.PVP_WIN_GOLDS
    exp = Static.PVP_WIN_EXP
    # hero_exp = Static.PVP_WIN_HERO_EXP
    # fragment = None
    # info = ""
    # target_info = ""
    # if fragmentId:
    #     info=u"抢夺:%s:%s" % (target_player.name, target_player.pk)
    #     target_info = u"被抢夺:%s:%s" % (player.name, player.pk)
    #     fragment = get_artifactfragment(fragmentId)

    #重置免战
    # if fragment and player.in_waravoid and target_player.pk > 0:
    #     player.reset_waravoid()

    if isWin:
        player.add_gold(golds, info=u"PVP")
        player.add_xp(exp)
        rewards.append({"type":Static.GOLD_ID, "count":golds})
        rewards.append({"type":Static.XP_ID, "count":exp})
        # if fragment:
        #     if target_player.pk < 0:
        #         is_robot = True
        #     else:
        #         is_robot = False
        #     grabprob = get_artifactfragment_grabprob(fragment.quality)
        #     new_prob = random.uniform(0, 100)
        #     #概率检查
        #     if is_robot and new_prob <= grabprob.robotProb:
        #             acquire_artifactfragment(player, fragment, number=1, info=info)
        #             rewards.append({"type":fragment.pk, "count":1})
        #     #真人、
        #     elif not is_robot and not target_player.in_waravoid and new_prob <= grabprob.playerProb:
        #         target_playerfragment = get_playerartifactfragment_by_fragment(target_player, fragment.pk)
        #         if target_playerfragment.sub(1, target_info):
        #             acquire_artifactfragment(player, fragment, number=1, info=info)
        #             modifydata = target_player.modifydata(True)
        #             if target_playerfragment.count > 0:
        #                 target_playerfragment.save()
        #                 modifydata.update_artifactfragment(target_playerfragment)
        #             else:
        #                 target_playerfragment.delete()
        #                 modifydata.delete_artifactfragment(fragmentId)
        #             modifydata.save()
        #             rewards.append({"type":fragment.pk, "count":1})

        # else:
        honor = Static.PVP_WIN_HONOR #荣誉点数
        player.PVP.add_honor(honor, info=u"PVP胜利结算")
        rewards.append({"type":Static.HONOR_ID, "count":honor})
        old_score = player.PVP.score
        get_score = player.PVP.win(target_player)
        rewards.append({"type":Static.SCORE_ID, "count":get_score})
    else:
        if not fragmentId:
            # player.PVP.serieWins = 0
            # rewards.append({"type":Static.SCORE_ID, "count":get_score})
            honor = Static.PVP_LOSE_HONOR #荣誉点数
            player.PVP.add_honor(honor, info=u"PVP失败结算")
            rewards.append({"type":Static.HONOR_ID, "count":honor})
            get_score = player.PVP.lose(target_player.PVP.score)
            rewards.append({"type":Static.SCORE_ID, "count":get_score})
        # else:
        #     yoyprint(u"抢夺碎片战斗结算失败")

    return rewards

def init_weekly_pvp_data():
    """
    初始化pvp每周数据
    """
    robotPlayers = Player.objects.filter(id__lt=0, id__gt=-10000, level__gte=Static.PVP_LEVEL)

    for robotPlayer in robotPlayers:
        robot = get_robot(robotPlayer.pk)
        robotPlayer.PVP.set_score(robot.score)


def send_weekly_pvp_rewards():
    """
    发放上周竞技场奖励
    """

    lastweek_pvpdata = []
    # 获取上周800积分到100000积分之间的玩家
    rank_datas = PVPRank.get_last_ranks_by_score(800, 100000)#假定最大上线10w分
    pvpRanks = get_pvpRanks()
    pvpRanks = sorted(pvpRanks, key = lambda x: x.rank)

    dateStr = str(datetime.datetime.now().today())
    for p_id, p_score in rank_datas:
        rewards = []
        if not p_id or p_id == "None":
            continue

        p_id = int(p_id)
        opp_player = get_player(p_id, False)
        lastweek_pvpdata.append(opp_player.pvp_view_data(last_rank=True))
        if p_id > 0: #非机器人
            if opp_player and opp_player.level >= Static.PVP_LEVEL:
                for pvpRank in pvpRanks:
                    if p_score >= pvpRank.score:
                        rewards = pvpRank.weeklyRewards
                        break

            if not rewards:
                break
            reward_list = []
            for reward in rewards:
                reward_list.append(reward.to_dict())

            print "%s: send Weekly PVP Rewards:player id %s player name %s send reward id %s" % (dateStr, opp_player.pk, opp_player.name, pvpRank.pk) 
            #发奖
            contents = []
            contents.append({
                "content": "fytext_300710",
                "paramList": [str(int(opp_player.PVP.lastWeekRank))],
            })
            
            send_system_mail(player=opp_player, sender=None, title="fytext_300724", contents=contents, rewards=reward_list)
    PlayerPVPLastWeekData.set_data(lastweek_pvpdata)


def send_daily_pvp_rewards():
    """
    发放昨天竞技场奖励
    """
    yesterday_pvpdata = []
    #删除之前数据
   # PlayerPVPYesterday.objects.all().delete()
    # 获取昨天1-500名
    rank_datas = PVPRank.get_yesterday_ranks(0, 499)

    date = datetime.datetime.now().isocalendar()
    dateStr = str(datetime.datetime.now().today())


    pvpRanks = get_pvpRanks()
    pvpRanks = sorted(pvpRanks, key = lambda x: x.rank)
    for rank, (p_id, p_score) in enumerate(rank_datas):
        rank += 1
        rewards = []
        if not p_id or p_id == "None":
            continue

        p_id = int(p_id)
        opp_player = get_player(p_id, False)
        yesterday_pvpdata.append(opp_player.pvp_view_data())

        #保存前一天数据
        #PlayerPVPYesterday.objects.create(pk=opp_player.pk, rank=rank, score=p_score)

        if p_id > 0: #非机器人
            if opp_player and opp_player.level >= Static.PVP_LEVEL:
                for pvpRank in pvpRanks:
                    if rank <= pvpRank.rank:
                        rewards = pvpRank.dailyRewards
                        break

            if not rewards:
                break
            reward_list = []
            for reward in rewards:
                reward_list.append(reward.to_dict())

            print "%s:send Daily PVP Rewards:player id %s player name %s send reward id %s" % (dateStr, opp_player.pk, opp_player.name, pvpRank.pk) 
            #发奖
            contents = []
            contents.append({
                "content": "fytext_300709",
                "paramList": [str(opp_player.PVP.yesterdayRank)],
            })
            send_system_mail(player=opp_player, sender=None, title="fytext_300723", contents=contents, rewards=reward_list)

    PlayerPVPYesterdayData.set_data(yesterday_pvpdata)
