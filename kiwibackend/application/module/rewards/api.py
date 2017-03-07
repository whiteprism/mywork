# -*- coding: utf-8 -*-
from playeritem.api import acquire_item
from playerequip.api import acquire_equip, acquire_equipfragment
from playerartifact.api import acquire_artifact, acquire_artifactfragment
from playersoul.api import acquire_soul
from playerhero.api import acquire_hero
from playerbuilding.api import acquire_buildingfragment
import re
from rewards.models import CommonReward

def get_commonreward(rewardIdStr):
    pattern = re.compile(r"t(\d+)v?(\d*)c?(\d*)")
    match = pattern.match(rewardIdStr)
    category = 0
    level = 0
    count = 0
    if match:
        category, level, count = match.groups()
        category = int(category) if category else 0
        level = int(level) if level else 0
        count = int(count) if count else 1

    reward = CommonReward(category, count, level)

    return reward


def reward_cost_check(player, reward, number=1):
    """
    奖励消耗检查
    """
    #英雄进阶消耗圣器
    if reward.is_artifact:
        raise
    elif reward.is_item:
        playeritem = player.items.get(reward.type)
        if playeritem:
            if playeritem.count < reward.count * number:
                return False
        else:
            return False
    elif reward.is_gold:
        if player.gold < reward.count * number:
            return False
    elif reward.is_yuanbo:
        if player.yuanbo < reward.count * number:
            return False
    elif reward.is_couragepoint:
        if player.couragepoint < reward.count * number:
            return False
    elif reward.is_honorpoint:
        if player.PVP.honor < reward.count * number:
            return False
    elif reward.is_buildingfragment:
        fragment = player.buildingfragments
        if not fragment:
            return False
        if fragment.get(reward.type).count < reward.count * number:
            return False
    return True

def reward_cost(player, reward, info=u"", number=1):
    """
    奖励消耗
    """
    #英雄进阶消耗圣器
    if reward.is_artifact:
        raise
    elif reward.is_item:
        playeritem = player.items.get(reward.type)
        playeritem.sub(reward.count * number, info=info)
    elif reward.is_gold:
        player.sub_gold(reward.count * number, info=info)
    elif reward.is_wood:
        player.sub_wood(reward.count * number, info=info)
    elif reward.is_yuanbo:
        player.sub_yuanbo(reward.count * number, info=info)
    elif reward.is_couragepoint:
        player.sub_couragepoint(reward.count * number, info=info)
    elif reward.is_honorpoint:
        player.PVP.sub_honor(reward.count * number, info=info)
        player.PVP_change = True
    elif reward.is_buildingfragment:
        player.buildingfragments.get(reward.type).sub(reward.count * number, info=info)

def reward_send(player, reward, info = u"", number=1):
    """
    奖励发放
    """
    _data = {}

    if reward.is_hero:
        for i in range(0, reward.count * number):
            star = int(str(reward.type)[-2:])
            heroId = reward.type / 100 * 100
            playerunit = acquire_hero(player, heroId, info=info, star=star)
            
            if playerunit.is_hero:
                _data[reward.type] = {
                    "type" : reward.type,
                    "count": 1
                }
            else:
                if reward.type not in _data:
                    _data[playerunit.soul_id] = {
                        "type" : playerunit.soul_id,
                        "count": 0       
                    }
                _data[playerunit.soul_id]["count"] += playerunit.soul.breakCost
    else:

        if reward.is_equip:
            for i in range(0, reward.count * number):
                acquire_equip(player, reward.type, info=info)
        elif reward.is_equipfragment:
            for i in range(0, reward.count * number):
                acquire_equipfragment(player, reward.type, info=info)
        elif reward.is_artifact:
            for i in range(0, reward.count * number):
                acquire_artifact(player, reward.type, info=info)
        elif reward.is_soul:
            acquire_soul(player, reward.type, reward.count * number, info=info)
        elif reward.is_artifactfragment:
            acquire_artifactfragment(player,reward.type, number=reward.count * number, info=info)
        elif reward.is_item:
            acquire_item(player, reward.type, number=reward.count * number, info=info)
        elif reward.is_gold:
            player.add_gold(reward.count * number, info=info)
        elif reward.is_tower:
            player.add_towerGold(reward.count * number, info=info)
        elif reward.is_yuanbo:
            player.add_yuanbo(reward.count * number, info=info)
        elif reward.is_wood:
            player.add_wood(reward.count * number, info=info)
        elif reward.is_couragepoint:
            player.add_couragepoint(reward.count * number, info=info)
        elif reward.is_guildgold:
            player.guild.add_gold(reward.count * number, info=info)
        elif reward.is_honorpoint:
            player.PVP.add_honor(reward.count * number, info=info)
            player.PVP_change = True
        elif reward.is_xp:
            player.add_xp(reward.count * number)
        elif reward.is_power:
            player.add_power(reward.count * number)
        elif reward.is_army:
            player.armies.acquire(reward.type, reward.count * number)
            player.armies_change = True
        elif reward.is_stamina:
            player.add_stamina(reward.count * number)
        elif reward.is_buildingfragment:
            acquire_buildingfragment(player, reward.type, reward.count * number)

        _data[reward.type] = {
            "type" : reward.type,
            "count": reward.count * number        
        }

    return _data
