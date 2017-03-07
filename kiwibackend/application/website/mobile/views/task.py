# -*- encoding:utf8 -*-

from decorators import require_player, handle_common
from module.common.static import Static, AlertID
from module.task.api import get_dailytask, get_task, get_seven_days_task, get_dailytask_activity,get_sevenDaysHalfPrice
from module.rewards.api import reward_send
from module.common.middleware import ErrorException, AlertHandler
from module.playeritem.api import acquire_item
from module.vip.api import get_vip
#from module.item.api import get_itemsuit

@handle_common
@require_player
def taskDailyReward(request, response):
    """
    日常任务领取
    """
    player = request.player
    task_id = getattr(request.logic_request, "taskId", 0)
    task_id = int(task_id)
    task = get_dailytask(task_id)

    if player.dailytask_is_done(task.category):
        player.dailytask_done(task.category)

        #扫荡券
        if task.is_vip_sweep:
            vip = get_vip(player.vip_level)
            acquire_item(player, Static.ITEM_SWEEP_ID, number=vip.sweepCount, info=u"VIP领取")
        else:
            for reward in task.rewards:
                reward_send(player,reward, info=u"日常任务领取")
    else:
        player.update_dailytask(task.category)
        AlertHandler(player, response, AlertID.ALERT_DAILYTASK_UNDONE,u"taskDailyReward:taskGid(%s) is not done" % (task_id))

    return response

@handle_common
@require_player
def taskReward(request, response):
    """
    任务领取
    """
    player = request.player
    task_id = getattr(request.logic_request, "taskId", 0)
    task_id = int(task_id)
    task = get_task(task_id)

    # 先来判断任务是否完成
    if player.task_is_done(task.category):
        player.task_done(task.category)
        for reward in task.rewards:
            reward_send(player, reward, info=u"任务领取")
    else:
        player.update_task(task.category)
        AlertHandler(player, response, AlertID.ALERT_TASK_UNDONE, u"taskReward:taskGid(%s) is not done" % (task_id))

    return response


@handle_common
@require_player
def sevenDaysTaskReward(request, response):
    """
    七天任务奖励领取
    """
    player = request.player
    task_id = getattr(request.logic_request, "taskId", 0)
    task_id = int(task_id)
    task = get_seven_days_task(task_id)

    # 先来判断任务是否完成

    if str(task_id) in player.completeSevenTasks and  player.completeSevenTasks[str(task_id)] == 0:
        player.completeSevenTasks[str(task_id)] = 1
        for reward in task.rewards:
            reward_send(player, reward, info=u"七天乐任务领取")
        player.set_update("completeSevenTasks")

    return response




@handle_common
@require_player
def dailyTaskActivityReward(request, response):
    """
    领取活跃度奖励
    """
    player = request.player
    activityId = getattr(request.logic_request, "activityId", 0)

    activity = get_dailytask_activity(activityId)

    if activityId in player.activityBoxIds:
        AlertHandler(player, response, AlertID.ALERT_DAILYTASK_REWARD_RECEIVED, u"dailyTaskActivityReward:activityId(%s) had received" % (activityId))
        return response

    if player.dailyTaskActivity < activity.activityValue:
        AlertHandler(player, response, AlertID.ALERT_DAILYTASK_ACTIVITY_NOT_ENOUGH, u"dailyTaskActivityReward:activity(%s) need (%s) player have (%s)" % (activityId, activity.activityValue, player.dailyTaskActivity))
        return response

    #　完成日常任务会获取活跃度

    player.activityBoxIds.append(activityId)
    player.set_update("activityBoxIds")

    for reward in activity.rewards:
        reward_send(player, reward, info=u"活跃度奖励")

    return response




@handle_common
@require_player
def sevenDaysHalfBuy(request, response):
    """
    七天乐半价购买
    """
    player = request.player


    sevenId = getattr(request.logic_request, "sevenId", 0)

    sevenPrice = get_sevenDaysHalfPrice(sevenId)

    if player.daysFromcreated > 9 or player.daysFromcreated < sevenId:
        AlertHandler(player, response, AlertID.ALERT_SEVENDAYS_IS_NOT_ALLOWED, u"sevenDaysHalfBuy:playerdays not between 1 and 9 had received" % (player.daysFromcreated))
        return response

    if sevenPrice.id in player.halfBuyIds:
        AlertHandler(player, response, AlertID.ALERT_SEVENDAYS_ONLY_ONCE, u"sevenDaysHalfBuy:this is item(%s) had buyed" % (sevenPrice.id))
        return response

    if player.yuanbo < sevenPrice.itemCost:
        AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"sevenDaysHalfBuy: sevenPrice cost (%s) and player has (%s)" % (sevenPrice.itemCost, player.yuanbo))
        return response

    reward_send(player, sevenPrice.reward, info=u"七天半价购买%s" %sevenPrice.id)


    player.halfBuyIds.append(sevenPrice.pk)
    player.set_update("halfBuyIds")

    player.sub_yuanbo(sevenPrice.itemCost,info=u"七天半价购买%s" %sevenPrice.id)

    response.common_response.player.set("halfBuyIds", player.halfBuyIds)
    if player.isOpenArena:
        response.common_response.player.set("arena", player.PVP.to_dict())

    return response
