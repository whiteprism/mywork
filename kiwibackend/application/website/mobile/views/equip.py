# -*- encoding:utf8 -*-
from decorators import require_player, handle_common
from module.common.static import Static, AlertID
from module.equip.api import get_equipenhance, get_equip, get_equipfragment, get_equiprefine
from module.common.middleware import ErrorException, AlertHandler
from module.common.actionlog import ActionLogWriter
from module.playerequip.api import acquire_equip
from module.playeritem.api import acquire_item
from module.item.api import get_item

@handle_common
@require_player
def equipUp(request, response):
    """
    装备or圣物穿戴
    """
    pos = getattr(request.logic_request, "pos", 0) #获取装备位置1-4装备，5-6 圣物
    is_equip = True if pos < 5 else False

    if is_equip:
        return _equipUp(request, response)
    else:
        return _artifactUp(request, response)

def _equipUp(request, response):
    """
    装备穿戴
    """
    playerequip_id = getattr(request.logic_request, "playerEquipId", 0)
    playerhero_id = getattr(request.logic_request, "playerHeroId", 0)
    pos = getattr(request.logic_request, "pos", 0) #获取装备位置1-4装备，5-6 圣物

    player = request.player

    #检查英雄
    playerhero = player.heroes.get(playerhero_id)
    if not playerhero:
        raise ErrorException(player, u"_equipUp:playerhero_id(%s) is not existed" % playerhero_id)

    pos = int(pos)
    #位置1~4 
    if not (1 <= pos <= 4):
        raise ErrorException(player, u"_equipUp:playerhero_id(%s) pos(%s) is error" % (playerhero_id, pos))

    playerequip = player.equips.get(playerequip_id)

    #检查装备
    if not playerequip:
        raise ErrorException(player, u"_equipUp:playerhero_id(%s) pos(%s) playerequip(%s) is not existed" % (playerhero_id, pos, playerequip_id))

    #装备类型检查
    if playerhero.warrior.hero.category not in playerequip.equip.heroTypeList:
        player.update_equip(playerequip)
        player.update_hero(playerhero)
        AlertHandler(player, response, AlertID.ALERT_EQUIP_HERO_TYPE_ERROR, u"_equipUp:playerhero_id(%s) pos(%s) playerequip(%s) can not weared error type" % (playerhero_id, pos, playerequip_id))
        return response

    #检查装备类型
    if not playerequip.equip.can_wear(pos):
        alert_id = AlertID.ALERT_EQUIP_CAN_NOT_WEAR
        AlertHandler(player, response, alert_id, u"_equipUp:playerhero_id(%s) pos(%s) playerequip(%s) can not weared" % (playerhero_id, pos, playerequip_id))
        return response

    #检查装备是否从其他英雄身上卸下来
    target_playerhero = None
    if playerequip.playerhero_id > 0:
        target_playerhero = player.heroes.get(playerequip.playerhero_id)
        target_playerhero.set_equip(pos, 0)
        player.update_hero(target_playerhero, True)

    #卸下装备数据更新
    target_playerequip_id = playerhero.get_equip(pos)
    if target_playerequip_id:
        target_playerequip = player.equips.get(target_playerequip_id)
        target_playerequip.playerhero_id = 0
        player.update_equip(target_playerequip, True)

    #对应英雄更新
    playerhero.set_equip(pos, playerequip)
    player.update_hero(playerhero, True)

    #对应装备更新
    playerequip.playerhero_id = playerhero.pk

    if player.tutorial_id == Static.TUTORIAL_ID_EQUIP_UP_4:
        player.tutorial_complete()

    player.update_equip(playerequip, True)
    return response

def _artifactUp(request, response):
    """
    圣物穿戴
    """
    playerequip_id  = getattr(request.logic_request, "playerEquipId", 0)
    playerhero_id = getattr(request.logic_request, "playerHeroId", 0)
    pos = getattr(request.logic_request, "pos", 0) #获取装备位置1-4装备，5-6 圣物

    player = request.player

    #检查英雄
    playerhero = player.heroes.get(playerhero_id)
    if not playerhero:
        raise ErrorException(player, u"_artifactUp:playerhero_id(%s) is not existed" % playerhero_id)

    pos = int(pos)
    if not (5 <= pos <= 6):
        raise ErrorException(player, u"_artifactUp:playerhero_id(%s) pos(%s) is error" % (playerhero_id, pos))

    playerartifact = player.artifacts.get(playerequip_id)
    #检查圣物
    if not playerartifact:
        raise ErrorException(player, u"_artifactUp:playerhero_id(%s) pos(%s) playerequip(%s) is not existed" % (playerhero_id, pos, playerequip_id))

    #检查装备类型
    if not playerartifact.artifact.can_wear(pos):
        alert_id = AlertID.ALERT_ARTIFACT_CAN_NOT_WEAR
        AlertHandler(player, response, alert_id, u"_artifactUp:playerhero_id(%s) pos(%s) playerequip(%s) can not weared" % (playerhero_id, pos, playerequip_id))
        return response

    #装备类型检查
    # if playerhero.warrior.hero.category not in playerartifact.artifact.heroTypeList:
    #     player.update_equip(playerartifact)
    #     player.update_hero(playerhero)
    #     AlertHandler(player, response, AlertID.ALERT_EQUIP_HERO_TYPE_ERROR, u"_equipUp:playerhero_id(%s) pos(%s) playerequip(%s) can not weared error type" % (playerhero_id, pos, playerequip_id))
    #     return response

    #检查装备是否从其他英雄身上卸下来
    target_playerhero = None
    if playerartifact.playerhero_id > 0:
        target_playerhero = player.heroes.get(playerartifact.playerhero_id)
        target_playerhero.set_equip(pos, 0)
        player.update_hero(target_playerhero, True)

    #卸下装备数据更新
    target_playerartifact_id = playerhero.get_equip(pos)
    target_playerartifact = None
    if target_playerartifact_id:
        target_playerartifact = player.artifacts.get(target_playerartifact_id)
        target_playerartifact.playerhero_id = 0
        player.update_artifact(target_playerartifact, True)

    #对应英雄更新
    playerhero.set_equip(pos, playerartifact)
    player.update_hero(playerhero, True)

    #对应装备更新
    playerartifact.playerhero_id = playerhero.pk
    player.update_artifact(playerartifact, True)

    return response

@handle_common
@require_player
def equipDown(request, response):
    """
    卸下装备or圣物
    """
    pos = getattr(request.logic_request, "pos", 0)
    is_equip = True if pos < 5 else False
    if is_equip:
        return _equipDown(request, response)
    else:
        return _artifactDown(request, response)

def _equipDown(request, response):
    """
    卸下装备
    """
    pos = getattr(request.logic_request, "pos", 0)
    playerhero_id = getattr(request.logic_request, "playerHeroId", 0)

    player = request.player

    #检查英雄
    playerhero = player.heroes.get(playerhero_id)
    if not playerhero:
        raise ErrorException(player, u"_equipDown:playerhero_id(%s) is not existed" % playerhero_id)

    pos = int(pos)
    #位置1~4   5,6为神器
    if not (1 <= pos <= 4):
        raise ErrorException(player, u"_equipDown:playerhero_id(%s) pos(%s) is error" % (playerhero_id, pos))

    playerequip_id = playerhero.get_equip(pos)
    playerequip = player.equips.get(playerequip_id)
    #检查装备
    if not playerequip:
        raise ErrorException(player, u"_equipDown:playerhero_id(%s) pos(%s) playerequip(%s) is not existed" % (playerhero_id, pos, playerequip_id))

    #对应英雄更新
    playerhero.set_equip(pos, 0)
    player.update_hero(playerhero, True)

    #对应装备更新
    playerequip.playerhero_id = 0
    player.update_equip(playerequip, True)

    return response

def _artifactDown(request, response):
    """
    卸下圣物
    """
    pos = getattr(request.logic_request, "pos", 0)
    playerhero_id = getattr(request.logic_request, "playerHeroId", 0)

    player = request.player

    #检查英雄
    playerhero = player.heroes.get(playerhero_id)
    if not playerhero:
        raise ErrorException(player, u"_artifactDown:playerhero_id(%s) is not existed" % playerhero_id)

    pos = int(pos)
    #位置1~4   5,6为神器
    if not (5 <= pos <= 6):
        raise ErrorException(player, u"_artifactDown:playerhero_id(%s) pos(%s) is error" % (playerhero_id, pos))


    playerartifact_id = playerhero.get_equip(pos)
    playerartifact = player.artifacts.get(playerartifact_id)
    #检查装备
    if not playerartifact:
        raise ErrorException(player, u"equipDown:playerhero_id(%s) pos(%s) playerequip(%s) is not existed" % (playerhero_id, pos, playerartifact_id))

    #对应英雄更新
    playerhero.set_equip(pos, 0)
    player.update_hero(playerhero, True)

    #对应装备更新
    playerartifact.playerhero_id = 0
    player.update_artifact(playerartifact, True)
    return response

@handle_common
@require_player
def equipLevelUp(request, response):
    
    """
    强化装备
    """
    delta_level = getattr(request.logic_request, "deltaLevel", 0) #升了多少级
    playerequip_id = getattr(request.logic_request, "playerEquipId", 0)

    player = request.player
    info = u"强化装备:%s" % playerequip_id

    playerequip = player.equips.get(playerequip_id)
    if not playerequip:
        raise ErrorException(player, u"equipLevelUp:playerequip_id(%s) is not existed" % playerequip_id)

    cost_gold = 0
    before_level = playerequip.level
    max_equip_level = player.level * 2
     
    #强化的次数
    for i in range(0, delta_level):  
        #装备等级不能超过人物等级2倍
        if playerequip.level >= max_equip_level:
            AlertHandler(player, response, AlertID.ALERT_LEVEL_NOT_ENOUGH, u"equipLevelUp:playerequip_id(%s) level(%s)  playerLevel(%s)" % (playerequip_id, playerequip.level, player.level))
            return response

        next_equipenhance = get_equipenhance(playerequip.level + 1)
        
        #没有下一个强化等级，已经强化到最高
        if not next_equipenhance: 
            raise ErrorException(player, u"equipLevelUp:playerequip_id(%s) level(%s) can not levelup" % (playerequip_id, playerequip.level))
        equipenhance = get_equipenhance(playerequip.level)
        playerequip.level_up(player, 1)
        cost_gold += equipenhance.gold

    after_level = playerequip.level
    #金币不足
    if player.gold < cost_gold: 
        AlertHandler(player, response, AlertID.ALERT_GOLD_NOT_ENOUGH, u"equipLevelUp:playerequip_id(%s) totalGold(%s)  playerGold(%s)" % (playerequip_id, cost_gold, player.gold))
        return response

    player.sub_gold(cost_gold, info)

    player.dailytask_going(Static.DAILYTASK_CATEGORY_ENHANCE, number=1, is_incr=True, is_series=True)
    ActionLogWriter.equip_enhance(player, playerequip.pk, playerequip.equip_id, before_level, after_level, info=info) 

    #如果是穿在身上的装备，判断是否出发强化大师。
    if playerequip.playerhero_id > 0:
        playerhero = player.heroes.get(playerequip.playerhero_id)
        if playerhero.check_equip_enhancemaster():
            player.update_hero(playerhero, True)
    player.update_equip(playerequip, True)
    return response

@handle_common
@require_player
def equipAutoLevelUp(request, response):
    
    """
    一键强化装备
    """
    playerequip_id = getattr(request.logic_request, "playerEquipId", 0)

    player = request.player
    info = u"一键强化装备:%s" % playerequip_id

    playerequip = player.equips.get(playerequip_id)
    if not playerequip:
        raise ErrorException(player, u"equipAutoLevelUp:playerequip_id(%s) is not existed" % playerequip_id)

    # 策划修改需求2016.5.31 修改。
    before_level = playerequip.level
    delta_level = player.level * 2 - playerequip.level
    max_equip_level = player.level * 2
    for i in range(0, delta_level):
        #if playerequip.level >= max_equip_level:
        #    AlertHandler(player, response, AlertID.ALERT_LEVEL_NOT_ENOUGH, u"equipLevelUp:playerequip_id(%s) level(%s)  playerLevel(%s)" % (playerequip_id, playerequip.level, player.level))
        #    return response


        next_equipenhance = get_equipenhance(playerequip.level + 1)
        equipenhance = get_equipenhance(playerequip.level)
        #对应英雄更新
        if not next_equipenhance:
            break

        if player.gold >= equipenhance.gold:
            player.sub_gold(equipenhance.gold, info)
        else:
            break

        playerequip.level_up(player, 1)

    after_level = playerequip.level

    ActionLogWriter.equip_enhance(player, playerequip.pk, playerequip.equip_id, before_level, after_level, info=info)
    player.dailytask_going(Static.DAILYTASK_CATEGORY_ENHANCE, number=1, is_incr=True, is_series=False)
    #强化大师检查
    if playerequip.playerhero_id > 0:
        playerhero = player.heroes.get(playerequip.playerhero_id)
        if playerhero.check_equip_enhancemaster():
            player.update_hero(playerhero, True)
    player.update_equip(playerequip, True)
    if player.tutorial_id == Static.TUTORIAL_ID_EQUIP_ENHANCE_6:
        player.tutorial_complete()

    return response

@handle_common
@require_player
def heroEquipsAutoLevelUp(request, response):
    
    """
    英雄一键强化装备
    """
    playerhero_id = getattr(request.logic_request, "playerHeroId", 0)

    player = request.player
    info = u"英雄一键强化装备:%s" % playerhero_id

    playerhero = player.heroes.get(playerhero_id)
    if not playerhero:
        raise ErrorException(player, u"heroEquipsAutoLevelUp:playerhero_id(%s) is not existed" % playerhero_id)

    playerequips = []
    rangelevel = 0
    is_break = False

    #只装备，不包括圣物
    for i in range(1,5):
        playerequip_id = playerhero.get_equip(i)

        #没有装备跳过
        if not playerequip_id:
            continue
        playerequip = player.equips.get(playerequip_id)
        if not playerequip:
            continue

        playerequips.append(playerequip)

    if playerequips:
        levels = [playerequip.level for playerequip in playerequips]
        for playerequip in playerequips:
            #if playerequip.level + Static.EQUIP_ENHANCE_STEP <= player.level * 2:
            #    rangelevel = Static.EQUIP_ENHANCE_STEP
            #else:

            rangelevel = player.level * 2 - playerequip.level

            max_equip_level = player.level * 2

            for i in range(rangelevel):

                #if playerequip.level >= max_equip_level:
                #   AlertHandler(player, response, AlertID.ALERT_LEVEL_NOT_ENOUGH, u"equipLevelUp:playerequip_id(%s) level(%s)  playerLevel(%s)" % (playerequip_id, playerequip.level, player.level))
                #    return response

                next_equipenhance = get_equipenhance(playerequip.level + 1)
                equipenhance = get_equipenhance(playerequip.level)
                if not next_equipenhance:
                    break
                if player.gold >= equipenhance.gold:
                    player.sub_gold(equipenhance.gold, info)
                    playerequip.level_up(player, 1)
                else:
                    is_break = True
                    break
            if is_break:
                break


        after_levels = [playerequip.level for playerequip in playerequips]
        for i, level in enumerate(levels):
            if after_levels[i] > level:
                playerequip = playerequips[i]
                ActionLogWriter.equip_enhance(player, playerequip.pk, playerequip.equip_id, level, after_levels[i], info=info) 
                player.update_equip(playerequip, True)

    if playerhero.check_equip_enhancemaster():
        player.update_hero(playerhero, True)
    player.dailytask_going(Static.DAILYTASK_CATEGORY_ENHANCE, number=1, is_incr=True, is_series=False)

    return response

@handle_common
@require_player
def equipCompose(request, response):
    """
    装备碎片合成装备
    """
    fragment_id = getattr(request.logic_request, "fragmentId", 0)

    player = request.player
    info = u"合成装备:%s" % fragment_id

    fragment = get_equipfragment(fragment_id)
    if not fragment:
        raise ErrorException(player, u"equipCompose:fragment(%s) is not existed" % fragment_id)

    equip = get_equip(fragment.equipId)
    if not equip:
        raise ErrorException(player, u"equipCompose:equip(%s) is not existed" % fragment.equipId)

    playerfragment = player.equipfragments.get(fragment.pk)
    if not playerfragment or not playerfragment.can_sub(fragment.composeCount):
        if not playerfragment:
            player.delete_equipfragment(fragment_id)
        else:
            player.update_equipfragment(playerfragment)
        AlertHandler(player, response, AlertID.ALERT_EQUIP_COMPOSE_FRAGMENT_NOT_ENOUGH, u"equipCompose:fragment(%s) composeCount(%s)" % (fragment_id, fragment.composeCount))
        return response

    player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_EQUIP_COMPOSE, number=1, is_incr=True, with_top=False, is_series=True)
    player.update_equipfragment(playerfragment)
    playerfragment.sub(fragment.composeCount, info=info)
    playerequip = acquire_equip(player, fragment.equipId, info=info)
    response.logic_response.set("playerEquipId", playerequip.pk)
    return response

@handle_common
@require_player
def equipRefine(request, response):
    """
    装备精炼
    """
    playerequip_id_leves = getattr(request.logic_request, "playerEquipIdLevels", 0)
    player = request.player

    playerequip_ids = playerequip_id_leves[0:len(playerequip_id_leves):2]
    playerequip_deltlevels = playerequip_id_leves[1:len(playerequip_id_leves):2]
    playerequip_dicts = dict(zip(playerequip_ids, playerequip_deltlevels))

    refine_item_id = Static.ITEM_REFINE_ID
    cost_refinexp = 0   #此次精炼一共需要的精炼经验，这个值会与玩家所携带的值做比较，小于玩家的，就精炼并扣除可以提供相应精炼的石头个数。

    for playerequip_id, playerequip_deltalevel in playerequip_dicts.items():
        playerequip = player.equips.get(playerequip_id)
        if not playerequip:
                AlertHandler(player, response, AlertID.ALERT_EQUIP_IS_NOT_EXISTS, u" playerequip(%s) is  not  existed" %playerequip_id)
        before_level = playerequip.refineLevel
        playerrefinestone = player.items.get(refine_item_id)  #获取玩家身上所有精炼的石头
        point = playerrefinestone.count * playerrefinestone.item.number   #用精炼石计算出当前玩家可以提供的精炼经验。

        for i in range(0, playerequip_deltalevel):
            equiprefine_next = get_equiprefine(playerequip.equip.quality, playerequip.refineLevel +1)
            equiprefine = get_equiprefine(playerequip.equip.quality, playerequip.refineLevel)

            if not equiprefine_next:
                AlertHandler(player, response, AlertID.ALERT_EQUIP_CAN_NOT_REFINE, u" equiprefineLevel(%s) is the top" %playerequip.refineLevel)
                return response

            if equiprefine.equipLevel > playerequip.level:
                AlertHandler(player, response, AlertID.ALERT_EQUIP_CAN_NOT_REFINE, u" equipLevel(%s) is lower than refineequiplevel(%s) " % (playerequip.level,playerequip.refineLevel))
                return response

            cost_refinexp += equiprefine.refineXp
            if cost_refinexp > point:
                AlertHandler(player, response, AlertID.ALERT_ITEM_NOT_ENOUGH, u"equipRefine:item_id(%s) number is not enough" %playerrefinestone.item_id)
                return response
            playerequip.refine(1)

            player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_ONE_EQUIP_REFINE, number=playerequip.refineLevel, is_incr=False, with_top=True, is_series=True)

            if playerequip.refineLevel == 5:
                player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_ALL_EQUIP_REFINE10, number=1, is_incr=True, with_top=False, is_series=False)

            elif playerequip.refineLevel == 3:
                player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_ALL_EQUIP_REFINE5, number=1, is_incr=True, with_top=False, is_series=False)

            #检查精炼大师
            if playerequip.playerhero_id > 0:
                playerhero = player.heroes.get(playerequip.playerhero_id)
                if playerhero.check_equip_refinemaster():
                    player.update_hero(playerhero, True)
    info = u"装备精炼" 
    ActionLogWriter.equip_refinelevelup(player, playerequip, before_level, playerequip.refineLevel, info)
    player.dailytask_going(Static.DAILYTASK_CATEGORY_REFINE, number=1, is_incr=True, is_series=True)
    player.update_equip(playerequip, True)
    count = cost_refinexp/playerrefinestone.item.number
    playerrefinestone.sub(count, info)

    return response

@handle_common
@require_player
def equipMelt(request, response):
    """
    装备回炉
    """
    playerequip_id = getattr(request.logic_request, "playerEquipId", 0)

    player = request.player

    playerequip = player.equips.get(playerequip_id)
    if not playerequip:
        raise ErrorException(player, u"equipMelt:playerequip_id(%s) is not existed" % playerequip_id)

    if not playerequip.can_melt:
        player.update_equip(playerequip)
        AlertHandler(player, response, AlertID.ALERT_EQUIP_CAN_NOT_MELT, u"equipMelt:playerequip_id(%s) can not melt" % (playerequip_id))
        return response

    #根据 装备分类，装备等级，精炼等级 计算回炉消耗的钻石。
    # diamond = Static.EQUIP_QUALITY_RATIO * playerequip.equip.quality + Static.EQUIP_LEVEL_RATIO * playerequip.level + Static.EQUIP_REFINELEVEL_RATIO * playerequip.refineLevel
    diamond = playerequip.equip.quality * (playerequip.level + playerequip.refineLevel * 4) / 5
    if player.yuanbo < diamond:
        AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"equipMelt:playerequip_id(%s)  melt costYuanbo(%s) playerYuanbo(%s)" % (playerequip_id, diamond, player.yuanbo))
        return response

    gold = 0
    refinexp = 0

    for i in range(1, playerequip.level):
        equipenhance = get_equipenhance(i)
        gold += equipenhance.gold

    for i in range(0, playerequip.refineLevel):
        equiprefine = get_equiprefine(playerequip.equip.quality, i)
        refinexp += equiprefine.refineXp

    info = u"装备回炉:%s:%s" % (playerequip_id, playerequip.equip_id)
    player.sub_yuanbo(diamond, info)
    playerequip.melt()
    rewards = []

    gold = int(Static.EQUIP_GOLD_RATIO * gold)

    player.add_gold(gold, info)
    rewards.append({"type": Static.GOLD_ID, "count": gold})

    refine_item_id = Static.ITEM_REFINE_ID
    refinepoint = get_item(refine_item_id).number
    number = refinexp/refinepoint
    if number > 0:
        acquire_item(player, refine_item_id, number=number, info=info)
        rewards.append({"type": refine_item_id, "count": number})

    #检查装备精炼大师 & 强化大师
    if playerequip.playerhero_id > 0:
        playerhero = player.heroes.get(playerequip.playerhero_id)

        # 之所以不用or将两个表达式相连是因为每个表达式里面有对应的操作，如果满足了第一个条件那么第二个就不会执行。
        check_refine = playerhero.check_equip_refinemaster()
        check_enhance = playerhero.check_equip_enhancemaster()
        if check_refine or check_enhance:
            player.update_hero(playerhero, True)

    player.update_equip(playerequip, True)
    response.logic_response.set("rewards", rewards)
    return response

@handle_common
@require_player
def equipDecompose(request, response):
    """
    装备分解
    """
    playerequip_ids = getattr(request.logic_request, "playerEquipIds", [])

    player = request.player

    rewards = []
    refine_item_id = Static.ITEM_REFINE_ID
    for playerequip_id in playerequip_ids:
        playerequip = player.equips.get(playerequip_id)
        if not playerequip:
            raise ErrorException(player, u"equipDecompose:playerequip_id(%s) is not existed" % playerequip_id)

        if not playerequip.can_decompose:
            player.update_equip(playerequip)
            AlertHandler(player, response, AlertID.ALERT_EQUIP_CAN_NOT_DECOMPOSE, u"equipDecompose： playerequip_id(%s) can not decompose" % (playerequip_id))
            return response

        refinexp = playerequip.equip.decomposeRefinePoint
        for i in range(0, playerequip.refineLevel):
            equiprefine = get_equiprefine(playerequip.equip.quality, i)
            refinexp += equiprefine.refineXp

        info = u"装备分解:%s:%s" % (playerequip_id, playerequip.equip_id)

        refinepoint = get_item(refine_item_id).number
        number = refinexp / refinepoint
        if number > 0:
            acquire_item(player, refine_item_id, number=number, info=info)
            rewards.append({"type": refine_item_id, "count": number})
        player.delete_equip(playerequip_id, True)
        ActionLogWriter.equip_delete(player, playerequip.pk, playerequip.equip_id, info)
    response.logic_response.set("rewards", rewards)

    return response
