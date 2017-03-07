# -*- coding: utf-8 -*-
from playeractivity.docs import PlayerActivity
from module.activity.api import get_activity, get_activity_by_type, get_open_activities
from module.common.static import Static
import datetime

def update_playeractivities(player):
    '''
    更新所有活动状态
    '''
    activities = get_open_activities(player)
    for activity in activities:
        update_playeractivity(player, activity)

def update_playeractivity(player, activity):
    '''
    根据活动更新活动状态
    '''
    is_new, playeractivity = player.activities.get_or_create(activity.id)
    if is_new:
        player.update_activity(playeractivity, True)

    if activity.category == Static.CONTINUOUS_LOGIN_TYPE:
        #每月第一天签到天数重置
        if datetime.datetime.now().date().strftime("%Y-%m") != playeractivity.updated_at.date().strftime("%Y-%m"):
            playeractivity.value1 = 1
            player.update_activity(playeractivity, True)
        elif datetime.datetime.now().date() != playeractivity.updated_at.date():
            #不是同一天 #每月清理, 并且前一天为领取状态
            if playeractivity.received:
                playeractivity.received = False
                playeractivity.value1 += 1
                player.update_activity(playeractivity, True)

#    elif activity.category == Static.NEWER_LEVEL_TYPE:
#        yoyprint(u"新手等级奖励更新")
#        pass
#    elif activity.category == Static.USER_GROW_UP:
#        yoyprint(u"用户成长奖励更新")
#        pass
#    elif activity.category == Static.POWER_RANK:
#        yoyprint(u"战斗力奖励更新")
#        pass
#    elif activity.category == Static.LEVEL_RANK: #等级竞赛
#        yoyprint(u"等级竞赛奖励更新")
#        pass
#    elif activity.category == Static.MONTH_CARD: #月卡
#        yoyprint(u"月卡剩余时间更新:%s,%s,%s" % ( datetime.datetime.now().date(), playeractivity.getTime.date(), playeractivity.value3))
#        if datetime.datetime.now().date() != playeractivity.getTime.date() and playeractivity.value3:
#            if datetime.datetime.now().date() >= playeractivity.endTime.date():
#                playeractivity.value3 = 0
#                playeractivity.received = False
#                yoyprint(u"月卡到期")
#            else:
#                playeractivity.received = False
#                playeractivity.value1 = (playeractivity.endTime.date() - datetime.datetime.now().date()).days
#                yoyprint(u"月卡还有天数:%s"% playeractivity.value1)
#            player.update_activity(playeractivity, True)
#


#def activate_month_card(player):
#    '''
#    激活月卡
#    '''
#    activity = get_activity_by_type(Static.MONTH_CARD)
#    _, playeractivity = player.activities.get_or_create(activity.id)
#    if playeractivity.value3:
#        yoyprint(u"月卡存在")
#        #存在月卡
#        if playeractivity.received:
#            add_day = 29 - playeractivity.value1
#        else:
#            #没领取
#            add_day = 30 - playeractivity.value1
#        yoyprint(u"add day : %s" % add_day)
#        playeractivity.endTime += datetime.timedelta(add_day)
#        playeractivity.value1 += add_day
#    else:
#        yoyprint(u"月卡不存在")
#        playeractivity.value2 = 1
#
#    player.update_activity(playeractivity, True)
#
#    return playeractivity

#def get_activity_rewards(player, activity_id, ruleValueInt):
#    '''
#    获得奖励
#    '''
#    isRight = False
#    rewards = []
#    data = {}
#    number = 1
#    activity = get_activity(activity_id)
#    if activity:
#        yoyprint(u"领取奖励的类型为:%s" % activity.category)
#        _, playeractivity = player.activities.get_or_create(activity.id)
#        if activity.category == Static.CONTINUOUS_LOGIN_TYPE and ruleValueInt == playeractivity.value1: #登录签到
#            #可能逻辑不同，分开写吧
#            if not playeractivity.received:
#                playeractivity.received = True
#                playeractivity.getTime = datetime.datetime.now()
#                player.update_activity(playeractivity, True)
#                #vip 等级高，奖励多倍
#                for rule in activity.rules:
#                    if rule.value1 == ruleValueInt:
#                        rewards = rule.giftPackage.rewards
#                        if player.vip_level >= rule.value2:
#                            number = rule.value3
#                        isRight = True
#                        break
#        elif activity.category == Static.NEWER_LEVEL_TYPE: #新手等级
#            #可能逻辑不同，分开写吧
#            if ruleValueInt <= player.level and ruleValueInt not in playeractivity.valueIntArray:
#                if playeractivity.checkGet(ruleValueInt):
#                    for rule in activity.rules:
#                        if rule.value1 == ruleValueInt:
#                            rewards = rule.giftPackage.rewards
#                            playeractivity.valueIntArray.append(ruleValueInt)
#                            player.update_activity(playeractivity, True)
#                            isRight = True
#                            break
#        elif activity.category == Static.LEVEL_RANK: #等级竞赛排位
#            #可能逻辑不同，分开写吧
#            pass
#        elif activity.category == Static.USER_GROW_UP: #用户成长
#            #可能逻辑不同，分开写吧
#            if playeractivity.received:
#                if ruleValueInt <= player.level and ruleValueInt not in playeractivity.valueIntArray:
#                    if playeractivity.checkGet(ruleValueInt):
#                        for rule in activity.rules:
#                            if rule.value2 == ruleValueInt:
#                                rewards = rule.giftPackage.rewards
#                                playeractivity.valueIntArray.append(ruleValueInt)
#                                player.update_activity(playeractivity, True)
#                                isRight = True
#                                break
#            else:
#                vip = get_vip(player.vip_level)
#                if vip.growthFund and player.yuanbo >= Static.GROW_GOLD_ACTIVITY_MOJO:
#                    player.sub_yuanbo(Static.GROW_GOLD_ACTIVITY_MOJO, info=u"成长基金")
#                    playeractivity.received = True
#                    player.update_activity(playeractivity, True)
#        elif activity.category == Static.MONTH_CARD: #月卡
#            if playeractivity.value2 and not playeractivity.value3:
#                #可以领取月卡
#                yoyprint(u"已经领取月卡")
#                playeractivity.endTime = datetime.datetime.now() + datetime.timedelta(30)
#                yoyprint(u"领取的月到到期的时间为:%s" % playeractivity.endTime)
#                playeractivity.value1 = 30 #可以领取剩余天数
#                playeractivity.value2 = 0 #不可以领取
#                playeractivity.value3 = 1 #已经领取过了
#                player.update_activity(playeractivity, True)
#            else:
#                #每天领取
#                if not playeractivity.received and playeractivity.value1:
#                    yoyprint(u"每天领取, 当前天数:%s"% playeractivity.value1)
#                    playeractivity.getTime = datetime.datetime.now()
#                    playeractivity.value1 -= 1
#                    playeractivity.received = True
#                    for rule in activity.rules:
#                        if rule.value1 == ruleValueInt:
#                            rewards = rule.giftPackage.rewards
#                            isRight = True
#                            break
#                    player.update_activity(playeractivity, True)
#
#    if not isRight:
#        rewards = []
#    data["rewards"] = rewards
#    data["number"] = number
#
#    return data

#def get_level_rank_rewards(player, level_rank):
#    '''
#    获取等级竞赛活动对应名次奖励
#    '''
#    activity = get_activity_by_type(Static.LEVEL_RANK)
#    rewards = []
#    if activity:
#        all_rules = sorted(activity.rules, key = lambda x: x.value1)
#        for rule in all_rules:
#            if level_rank >= rule.value1 and (level_rank <= rule.value2 or rule.value2==0) and player.level >= rule.value3:
                #todo value3???? 15 ??? 等级大于15
#                rewards = rule.giftPackage.rewards
#                break
#    return rewards

