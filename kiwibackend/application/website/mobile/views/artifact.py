 # -*- encoding:utf8 -*-
from decorators import require_player, handle_common
from module.common.static import Static, AlertID
from module.common.middleware import ErrorException, AlertHandler
from module.artifact.api import get_artifact, get_artifactenhance, get_artifactrefine, get_artifactfragment
from module.playerartifact.api import acquire_artifact
from playeritem.api import acquire_item
from module.common.actionlog import ActionLogWriter
from module.item.api import get_item

@handle_common
@require_player
def artifactLevelUp(request, response):
    """
    圣器强化
    """

    # 强化功能需要消耗同类型的圣物。其他的消耗品没有。

    #圣物强化素材的id
    material_playerartifact_ids = getattr(request.logic_request, "materialArtifactIds", [])
    playerartifact_id = getattr(request.logic_request, "artifactId", 0)

    player = request.player

    playerartifact = player.artifacts.get(playerartifact_id)
    if not playerartifact:
        raise ErrorException(player, u"artifactLevelUp:playerartifact(%s) is not existed" % playerartifact_id)

    xps = 0
    for _id in material_playerartifact_ids:
        material_playerartifact = player.artifacts.get(int(_id))
        if not material_playerartifact:
            raise ErrorException(player, u"artifactLevelUp:playerartifact(%s) materialArtifact(%s) is not existed" % (playerartifact_id, _id))

        # 穿在身上的不能作为强化素材。
        if material_playerartifact.is_weared:#是否装备
            raise ErrorException(player, u"artifactLevelUp:playerartifact(%s) materialArtifact(%s) is weared(%s)" % (playerartifact_id, _id,material_playerartifact.playerhero_id))

        # 强化素材一定是和被强化的是同类型的，或者可以是各种锭。
        if material_playerartifact.artifact.category != playerartifact.artifact.category and material_playerartifact.artifact.category != 9:
            raise ErrorException(player, u"artifactLevelUp:playerartifact(%s) materialArtifact(%s) type is not match" % (playerartifact_id, material_playerartifact))

        # 计算这件强化材料一共携带的经验
        delta_xps = material_playerartifact.xp
        for i in range(1, material_playerartifact.level):
            artifactenchance = get_artifactenhance(material_playerartifact.artifact.quality, i)
            delta_xps += artifactenchance.xp

        # 前一部分是材料以前经过强化所携带的经验，后一部分是它作为材料能够提供的基础经验，每一个圣物都有一个基础经验
        xps += int(delta_xps * Static.ARTIFACT_ENHANCE_XP_RATIO) + material_playerartifact.artifact.upgradeXp
        # 删除材料
        info = u"圣物强化消耗:%s" %playerartifact_id
        player.delete_artifact(material_playerartifact.pk, True)
        artifact = material_playerartifact.artifact
        ActionLogWriter.artifact_delete(player, _id, artifact, info)
     

    playerartifact.level_up(xps)

    #圣物强化大师
    if playerartifact.playerhero_id > 0:
        playerhero = player.heroes.get(playerartifact.playerhero_id)
        if playerhero.check_artifact_enhancemaster():
            player.update_hero(playerhero, True)

    player.task_going(Static.TASK_CATEGORY_ARTIFACT_LEVELUP, number=playerartifact.level, is_incr=False, is_series=True, with_top=True)
    player.update_artifact(playerartifact, True)

    return response

@handle_common
@require_player
def artifactRefine(request, response):
    """
    圣器精炼
    """
    playerartifact_id = getattr(request.logic_request, "artifactId", 0)
    # materialartifact_ids = getattr(request.logic_request, "artifactIds", []) #素材

    player = request.player

    playerartifact = player.artifacts.get(playerartifact_id)
    if not playerartifact:
        raise ErrorException(player, u"artifactRefine:playerartifact(%s) is not existed" % playerartifact_id)

    next_artifactrefine = get_artifactrefine(playerartifact.artifact.quality, playerartifact.refineLevel + 1)

    #已经精炼到顶级
    if not next_artifactrefine:
        AlertHandler(player, response, AlertID.ALERT_ARTIFACT_CAN_NOT_REFINE, u"artifactRefine:playerartifact(%s) refineLevel(%s) is the max  refinelevel" % (playerartifact_id, playerartifact.refineLevel))
        return response

    artifactrefine = get_artifactrefine(playerartifact.artifact.quality, playerartifact.refineLevel)

    #玩家等级不够
    if artifactrefine.playerLevel > player.level:
        AlertHandler(player, response, AlertID.ALERT_ARTIFACT_CAN_NOT_REFINE, u"artifactrefine:playerartifact(%s) player_level(%s) > player_level(%s)" %(playerartifact_id, artifactrefine.playerLevel, player.level))
        return response

    # 精炼消耗精炼石
    refine_item_id = Static.ARTIFACRT_REFINE_LIST[0]
    playeritem = player.items.get(refine_item_id)

    if artifactrefine.refineCost > playeritem.count * playeritem.item.number:
        AlertHandler(player, response, AlertID.ALERT_ITEM_NOT_ENOUGH, u"artifactRefine:playerartifact(%s) costMaterialCore(%s) > playerMaterialCore(%s)" % (playerartifact_id, artifactrefine.refineCost, playeritem.count * playeritem.item.number))
        return response

    playerartifact.refine()
    info = u"圣物精炼消耗:%s" %playerartifact_id
    count = artifactrefine.refineCost/playeritem.item.number
    playeritem.sub(count, info)

    #圣物精炼大师
    if playerartifact.playerhero_id > 0:
        playerhero = player.heroes.get(playerartifact.playerhero_id)
        if playerhero.check_artifact_refinemaster():
            player.update_hero(playerhero, True)

    player.update_artifact(playerartifact, True)
    return response

@handle_common
@require_player
def artifactCompose(request, response):
    """
    圣器合成
    """
    artifact_id = getattr(request.logic_request, "artifactId", 0)#圣器碎片ID
    info = u"合成圣器:%s" % artifact_id
    player = request.player
    #圣物合成需要该圣物的碎片
    fragment = get_artifactfragment(artifact_id)
    if not fragment:
        raise ErrorException(player, u"artifactCompose:fragment(%s) is not existed" % artifact_id)

    artifact = get_artifact(fragment.artifactId)
    if not artifact:
        raise ErrorException(player, u"artifactCompose:artifact(%s) is not existed" % fragment.artifactId)

    playerfragment = player.artifactfragments.get(fragment.pk)
    if not playerfragment or not playerfragment.can_sub(fragment.composeCount):
        if not playerfragment:
            player.delete_artifactfragment(artifact_id)
        AlertHandler(player, response, AlertID.ALERT_ARTIFACT_COMPOSE_MATERIAL_NOT_ENOUGH, u"artifactCompose:fragment(%s) composeCount(%s)" % (artifact_id, fragment.composeCount))
        return response
    player.update_artifactfragment(playerfragment)
    playerfragment.sub(fragment.composeCount, info=info)
    playerartifact = acquire_artifact(player, fragment.artifactId, info=info)
    response.logic_response.set("artifactId", playerartifact.pk)

    return response

@handle_common
@require_player
def artifactMelt(request, response):
    """
    圣物回炉
    """
    playerartifact_id = getattr(request.logic_request, "artifactId", 0)
    player = request.player

    playerartifact = player.artifacts.get(playerartifact_id)
    if not playerartifact:
        raise ErrorException(player, u"artifactMelt:playerartifact_id(%s) is not existed" % playerartifact_id)

    if not playerartifact.can_melt:
        AlertHandler(player, response, AlertID.ALERT_ARTIFACT_CAN_NOT_MELT, u"artifactMelt:playerartifact_id(%s) can not melt" % (playerartifact_id))
        return response

    #计算消耗钻石的总量
    diamond = playerartifact.artifact.quality * (playerartifact.level - 1 + playerartifact.refineLevel * 4)
    if player.yuanbo < diamond:
        AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"arrifactMelt:playerartifact_id(%s)  melt costDiamond(%s) >  playerYuanbo(%s)" % (playerartifact_id, diamond, player.yuanbo))
        return response

    materialcore = 0
    for i in range(0, playerartifact.refineLevel):
        artifactrefine = get_artifactrefine(playerartifact.artifact.quality, i)
        materialcore += artifactrefine.refineCost

    info = u"圣物回炉:%s" % playerartifact.pk

    rewards = []

    item_id = Static.ARTIFACRT_REFINE_LIST[0]
    item = get_item(item_id)
    number = materialcore/item.number

    #精炼石奖励
    if number > 0:
        acquire_item(player, item_id, number=number, info=info)
    rewards.append({"type": item_id, "count": number})
    #板砖奖励
    artifacts = Static.ARTIFACT_FRAGMENG_GRAB_LIST[:]
    artifacts.reverse() # 从最大经验的板砖开始
    total_xp = playerartifact.xp
    for i in range(1, playerartifact.level):
        total_xp += get_artifactenhance(playerartifact.artifact.quality, i).xp
    for artifact_id in artifacts:
        artifact = get_artifact(artifact_id)
        reward_count, left_xp = divmod(total_xp, artifact.upgradeXp)
        left_xp = total_xp%artifact.upgradeXp

        if reward_count > 0:
            acquire_artifact(player, artifact_id, info=info)
            rewards.append({"type": artifact_id, "count": reward_count})
        if left_xp == 0:
            break
        total_xp = left_xp

    player.sub_yuanbo(diamond, info)
    playerartifact.melt()
    ActionLogWriter.artifact_melt(player, playerartifact, info)
    #装备精炼大师&强化大师检查
    if playerartifact.playerhero_id > 0:
        playerhero = player.heroes.get(playerartifact.playerhero_id)
        # 之所以不用or将两个表达式相连是因为每个表达式里面有对应的操作，如果满足了第一个条件那么第二个就不会执行。
        is_refine = playerhero.check_artifact_refinemaster()
        is_enhance = playerhero.check_artifact_enhancemaster()
        if is_refine or is_enhance:
            player.update_hero(playerhero, True)

    player.update_artifact(playerartifact, True)

    response.logic_response.set("rewards", rewards)

    return response
