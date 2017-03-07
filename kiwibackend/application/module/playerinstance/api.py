# -*- coding:utf-8 -*-
from module.playerinstance.docs import PlayerInstanceLevel, PlayerEliteInstanceLevel, PlayerRaidInstance
from module.instance.api import get_instance, get_instancelevel, get_eliteinstancelevel, get_raidinstances, get_instancelevels_by_instance_id,get_eliteinstancelevel_by_instance_id
from module.common.static import Static
from module.vip.api import get_vip
from module.experiment.api import check_player_in_experiment_by_experimentname
import datetime

def get_player_open_raidinstance(player):
    '''
    过去开放的活动副本数据
    '''
    open_player_raidinstances = []
    # 先取得所有活动副本的信息。
    raidinstances = get_raidinstances()
    for raidinstance in raidinstances:
        # 通过里面的experiment1这个字段取判断活动副本是否开启
        if not raidinstance.experiment1 or check_player_in_experiment_by_experimentname(player.id, raidinstance.experiment1):
            _, playerraidinstance = player.raidinstances.get_or_create(raidinstance.id)
            data = {}
            data["type"] = playerraidinstance.level_id
            data["playCount"] = playerraidinstance.succeedCount
            # 根据ｖｉｐ等级限定次数
            vip = get_vip(player.vip_level)
            data["maxCount"] = vip.titanCount
            data["isDouble"] = check_player_in_experiment_by_experimentname(player.id, raidinstance.experiment2)
            open_player_raidinstances.append(data)

    return open_player_raidinstances

def get_all_player_star_by_instance_id(player, instance_id, isElite = False):
    '''
    获取玩家该章节的所有星级
    '''

    # 这个方法是用来获取玩家的所有星星数量验证是否能开启宝箱
    if isElite:
        instancelevels = get_eliteinstancelevel_by_instance_id(instance_id)
    else:
        instancelevels = get_instancelevels_by_instance_id(instance_id)

    star = 0
    for instancelevel in instancelevels:
        if isElite:
            playerinstancelevel = player.eliteinstancelevels.get(instancelevel.pk)
        else:
            playerinstancelevel = player.instancelevels.get(instancelevel.pk)

        if playerinstancelevel:
            star += playerinstancelevel.star

    return star

def get_update_instance_dict(player):
    '''
    获取玩家关卡数据
    '''
    viewDict = {}
    history_new_list = []
    history_list = []
    star_list = []
    elite_star_list = []

    if not player._update_list["instancelevels"] and not player._update_list["eliteinstancelevels"]:
        return None

    for pk in player._update_list["instancelevels"]:
        playerinstancelevel = player.instancelevels.get(pk)
        star_list.append(pk)
        star_list.append(playerinstancelevel.star)
        history_list.append(pk)
        history_list.append(playerinstancelevel.succeedCount)
        history_list.append(playerinstancelevel.refreshCount)

    for pk in player._update_list["eliteinstancelevels"]:
        playerinstancelevel = player.eliteinstancelevels.get(pk)
        elite_star_list.append(pk)
        elite_star_list.append(playerinstancelevel.star)
        history_new_list.append(pk)
        history_new_list.append(playerinstancelevel.succeedCount)
        history_new_list.append(playerinstancelevel.refreshCount)

    viewDict["lastFinished"] = player.lastInstance["lastFinished"] 
    viewDict["lastLevelId"] = player.lastInstance["lastLevelId"] 
    viewDict["lastEliteFinished"] = player.lastEliteInstance["lastEliteFinished"]
    viewDict["lastEliteLevelId"] = player.lastEliteInstance["lastEliteLevelId"]
    viewDict["history"] = history_list
    viewDict["starData"] = star_list
    viewDict["historyNew"] = history_new_list
    viewDict["eliteStarData"] = elite_star_list

    return viewDict


def get_player_view_instance_dict(player):
    '''
    获取玩家前端viewInstance的字典
    '''
    viewDict = {}
    viewDict["lastFinished"] = player.lastInstance["lastFinished"] 
    viewDict["lastLevelId"] = player.lastInstance["lastLevelId"] 
    viewDict["lastEliteFinished"] = player.lastEliteInstance["lastEliteFinished"]
    viewDict["lastEliteLevelId"] = player.lastEliteInstance["lastEliteLevelId"]

    playerinstancelevels = player.instancelevels.all()
    playereliteinstancelevels = player.eliteinstancelevels.all()

    history_list = []
    history_new_list = []
    star_list = []
    elite_star_list = []
    for level_id, playerinstancelevel in playerinstancelevels.items():
        history_list.append(level_id)
        history_list.append(playerinstancelevel.succeedCount)
        history_list.append(playerinstancelevel.refreshCount)
        star_list.append(level_id)
        star_list.append(playerinstancelevel.star)

    viewDict["history"] = history_list
    viewDict["starData"] = star_list
    for level_id, playereliteinstancelevel in playereliteinstancelevels.items():
        history_new_list.append(level_id)
        history_new_list.append(playereliteinstancelevel.succeedCount)
        history_new_list.append(playereliteinstancelevel.refreshCount)
        elite_star_list.append(level_id)
        elite_star_list.append(playereliteinstancelevel.star)

    viewDict["historyNew"] = history_new_list
    viewDict["eliteStarData"] = elite_star_list

    return viewDict



def get_chest_rewards(player, instanceId, chestLevel, isElite=False):
    '''
    获取宝箱奖励
    '''
    rewards_data = []
    if chestLevel > 2:
        chestLevel = 2
    instance = get_instance(instanceId)
    if not isElite:
        rewards_data = instance.boxData[chestLevel]
    else:
        rewards_data = instance.eliteBoxData[chestLevel]

    return rewards_data

def get_star(deadCount):
    '''
    根据死亡个数获得星级
    '''
    if deadCount == 0:
        return 3
    elif deadCount == 1:
        return 2
    return 1

def _debug_open_player_instance_at_instance_id(player, stop_instancelevel_id):
    """
    DEBUG 解锁玩家副本
    """
    instancelevel_id = Static.FIRST_INSTANCE_LEVEL_ID


    playerinstancelevels = player.instancelevels.all()
    for level_id, playerinstancelevel in playerinstancelevels.items():
        player.instancelevels.delete(playerinstancelevel.pk)

    while True:
        instancelevel = get_instancelevel(instancelevel_id)
        playerinstancelevel = PlayerInstanceLevel.unlock(player, instancelevel.id)
        playerinstancelevel.success(3)
        player.instancelevels.update(playerinstancelevel)
        instancelevel_id = instancelevel.nextInstanceId
        if instancelevel_id > stop_instancelevel_id:
            break

def unlock_player_instancelevel(player, level_id):
    playerinstancelevel = PlayerInstanceLevel.unlock(player, level_id)
    return playerinstancelevel

def _debug_open_player_eliteinstance_at_instance_id(player, stop_instancelevel_id):
    """
    DEBUG 解锁玩家副本
    """
    instancelevel_id = Static.FIRST_ELITE_INSTANCE_LEVEL_ID

    playerinstancelevels = player.eliteinstancelevels.all()
    for level_id, playerinstancelevel in playerinstancelevels.items():
        player.eliteinstancelevels.delete(playerinstancelevel.pk)

    while True:
        instancelevel = get_eliteinstancelevel(instancelevel_id)
        playerinstancelevel = PlayerEliteInstanceLevel.unlock(player, instancelevel.id)
        playerinstancelevel.success(3)
        player.eliteinstancelevels.update(playerinstancelevel)
        instancelevel_id = instancelevel.eliteNextInstanceId
        if instancelevel_id > stop_instancelevel_id:
            break
