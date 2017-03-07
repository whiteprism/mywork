# -*- encoding:utf8 -*-
from decorators import require_player, handle_common
from module.rewards.api import reward_send
from rewards.models import CommonReward

@handle_common
@require_player
def activityReward(request, response):

    """
    领取活动奖励
    """
    activityId = getattr(request.logic_request, "activityId", 0)
    param = getattr(request.logic_request, "param", 0)

    player = request.player

    _, playeractivity = player.activities.get_or_create(activityId)

    if playeractivity.activity.isCountinueLogin and not playeractivity.activity.isOpen(player.userid):
        raise ErrorException(player, u"activityReward:activityId:%s is ERROR" % activityId)

    data = playeractivity.get_rewards(param)

    rewards = data["rewards"]
    number = data["number"]

    view_rewards = []
    info = u"领取活动(%s:%s)奖励" % (activityId, param)
    for reward in rewards:
        reward_send(player, reward, info=info, number=number)
        rewardDict = reward.to_dict()
        rewardDict["count"] = reward.count * number
        view_rewards.append(rewardDict)

    response.logic_response.set("rewards",view_rewards)
    return response

@handle_common
@require_player
def loginBoxReward(request, response):
    """
    领取登陆宝箱奖励
    """
    activityId = getattr(request.logic_request, "activityId", 0)
    param = getattr(request.logic_request, "param", 0)

    player = request.player

    _, playeractivity = player.activities.get_or_create(activityId)

    if not playeractivity.activity.isCountinueLogin or not playeractivity.activity.isOpen(player.userid):
        raise ErrorException(player, u"loginBoxReward:activityId:%s" % activityId)

    rewards = playeractivity.get_login_boxrewards(param)

    view_rewards = []
    info = u"领取连续登陆(%s:%s)宝箱奖励" % (activityId, param)
    for reward in rewards:
        reward_send(player, reward, info=info)
        # 为了使前端的奖励数据看起来正常
        reward.count = reward.count
        view_rewards.append(reward.to_dict())

    response.logic_response.set("rewards",view_rewards)
    return response

@handle_common
@require_player
def offlineRewardGet(request, response):
    player = request.player

    if not player.offlinebonus:
        return response

    rewards = player.offlinebonus

    view_rewards = []
    info = u"离线奖励"
    for reward in rewards:
        tmp_reward = CommonReward(reward["type"], reward["count"], 0)
        reward_send(player, tmp_reward, info=info)
        view_rewards.append(tmp_reward.to_dict())
    player.offlinebonus = []
    player.set_update("offlinebonus")
    response.logic_response.set("rewards",view_rewards)
    response.common_response.player.set("offlinebonus",player.offlinebonus)
    return response
