# -*- encoding:utf8 -*-

from decorators import require_player, handle_common

from module.gashapon.api import get_gashapon, get_tavern
from module.common.static import Static, AlertID
from module.playerhero.api import  acquire_hero
from module.soul.api import get_soul
from module.hero.api import get_card, get_warrior
from module.skill.api import get_skilllevel, get_skilllevels_by_skill
from module.rewards.api import reward_cost_check, reward_cost, reward_send
from module.common.middleware import ErrorException, AlertHandler
from module.common.actionlog import ActionLogWriter
from module.hero.api import get_heroskill, get_herostarupgrade, get_herodestiny, get_heroteamlevel,get_heroteamlevel_by_teamid_level
from module.playeritem.api import acquire_item
from module.item.api import get_items
from module.soul.api import get_souls
from module.equip.api import get_equips, get_equipfragments
from module.playerequip.api import acquire_equip, acquire_equipfragment
from module.artifact.api import get_artifacts, get_artifactfragments
from module.playerartifact.api import acquire_artifact, acquire_artifactfragment
from module.playersoul.api import acquire_soul
import random

@handle_common
@require_player
def heroGacha(request, response):

    player = request.player
    is_ten = getattr(request.logic_request, "isTen", False)
    tavernId = getattr(request.logic_request, "tavernId", 0)
    rewards = []

    # 这个是先判断是什么抽奖，是金币还是钻石类型。
    tavern = get_tavern(tavernId)

    if not tavern:
        raise ErrorException(player, u"heroGacha:no tavern(%s)" % tavernId)

    else:
        #第一次十连抽使用ID = 3的抽奖配置
        if tavern.is_diamond and player.isFirstTenGacha and is_ten:
            gashapon_id = 3
        else:
            gashapon_id = tavern.gashapon_id

        gashapon = get_gashapon(gashapon_id)
        is_new, playergashapon = player.gashapons.get_or_create(gashapon.pk)

        playerGashaponItem = None

        # 如果是金币
        if tavern.is_gold:
            # 不是十连抽
            if not is_ten:
                #
                if not player.gashapon_is_gold_free and not reward_cost_check(player, tavern.tavern_cost):
                    AlertHandler(player, response, AlertID.ALERT_GOLD_NOT_ENOUGH, u"heroGacha:tavern(%s) needGold(%s) playerGold(%s)" % (tavern.pk, tavern.tavern_cost.count , player.gold))
                    return response
            else:
                if not reward_cost_check(player, tavern.tavern_tencost):
                    AlertHandler(player, response, AlertID.ALERT_GOLD_NOT_ENOUGH, u"heroGacha:tavern(%s) needGold(%s) playerGold(%s)" % (tavern.pk, tavern.tavern_tencost.count, player.gold))
                    return response
        else:
            if not is_ten:
                playerGashaponItem = player.items.get(Static.ITEM_DIAMOND_GASHAPON_ID)
                if not playerGashaponItem or not playerGashaponItem.can_sub(1):
                    if not player.gashapon_is_yuanbo_free and not reward_cost_check(player, tavern.tavern_cost):
                        AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"heroGacha:tavern(%s) needYuanbo(%s) playerYuanbo(%s)" % (tavern.pk, tavern.tavern_cost.count , player.yuanbo))
                        return response
            else:
                if  not reward_cost_check(player, tavern.tavern_tencost):
                    AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"heroGacha:tavern(%s) needYuanbo(%s) playerYuanbo(%s)" % (tavern.pk, tavern.tavern_tencost.count , player.yuanbo))
                    return response

        if tavern.is_gold:
            if not is_ten and player.gashapon_is_gold_free:
                player.use_gashapon_gold_free()
            else:
                if is_ten:
                    reward_cost(player, tavern.tavern_tencost, info=u"抽奖:%s:%s" % (gashapon.name, is_ten))
                else:
                    reward_cost(player, tavern.tavern_cost, info=u"抽奖:%s:%s" % (gashapon.name, is_ten))

        else:
            if not is_ten and player.gashapon_is_yuanbo_free:
                player.use_gashapon_yuanbo_free()
            else:
                if is_ten:
                    reward_cost(player, tavern.tavern_tencost, info=u"抽奖:%s:%s" % (gashapon.name, is_ten))
                else:
                    if not playerGashaponItem or not playerGashaponItem.can_sub(1):
                        reward_cost(player, tavern.tavern_cost, info=u"抽奖:%s:%s" % (gashapon.name, is_ten))
                    else:
                        playerGashaponItem.sub(1, info=u"英雄单抽卡")


        # 新手引导的话就只有新手引导，否则就走其他的抽奖
        if player.tutorial_id == Static.TUTORIAL_ID_GASHAPON_2 and player.tutorial['status'] != 2:
            playerhero = acquire_hero(player, 112000400, u"新手引导", star = 6)
            playerhero.gashapon_number = 1
            units = [playerhero]
            player.tutorial_complete()
            player.next_tutorial_open()
        else:
            if is_ten:
                gashapon_count = 10
                if not tavern.is_gold:
                    player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_GASHAPON, number=1, is_incr=True, with_top=False, is_series=True)
                    player.tenDiamondCount += 1

                    player.set_update("tenDiamondCount")
            else:
                gashapon_count = 1
            units = playergashapon.acquire(player, gashapon, count=gashapon_count)

        
        #第一次十连抽使用ID = 3的抽奖配置
        if tavern.is_diamond and player.isFirstTenGacha and is_ten:
            player.useFirstTenGacha()

        player.gashapons.update(playergashapon)
        player.dailytask_going(Static.DAILYTASK_CATEGORY_GASHAPON, number=len(units), is_incr=True, is_series=True)#召唤大师

    if is_ten and tavern.tenReward:
        reward_send(player, tavern.tenReward, info=u"%s:10连抽" % tavern.pk)

    elif not is_ten and tavern.reward:
        reward_send(player, tavern.reward, info=u"%s:单抽" % tavern.pk)

    for unit in units:
        reward = {"count":unit.gashapon_number, "type": unit.obj_id}
        if hasattr(unit, "from_hero"):
            reward["fromHero"] = unit.from_hero
        else:
            reward["fromHero"] = False

        rewards.append(reward)

    response.common_response.player.set("tavern", player.tavern)
    response.logic_response.set("rewards", rewards)

    return response

@handle_common
@require_player
def heroLevelUp(request, response):
    """
    英雄升级
    """
    playerhero_id = getattr(request.logic_request, "playerHeroId", 0)
    item_ids = getattr(request.logic_request, "itemIds", 0)

    player = request.player
    info = u"英雄升级:%s" % playerhero_id

    playerhero = player.heroes.get(playerhero_id)

    if not playerhero:
        raise ErrorException(player, u"heroLevelUp:playerhero(%s) is not existed" % (playerhero_id))

    items = dict(zip(item_ids[0:len(item_ids):2], item_ids[1:len(item_ids):2]))


    total_xp = 0

    for item_id, count in items.items():
        playeritem = player.items.get(item_id)
        if not playeritem:
            raise ErrorException(player, u"heroLevelUp:playeritem(%s) no existed" % (item_id))

        if not playeritem.can_sub(count):
            #更新数据
            player.update_item(playeritem)
            AlertHandler(player, response, AlertID.ALERT_ITEM_NOT_ENOUGH,  u"heroLevelUp:item(%s) playeritem(%s) useCount(%s) count(%s)" % (playeritem.item_id, item_id, count, playeritem.count))
            return response

        total_xp += playeritem.item.number * count

    playerhero.add_xp(total_xp,player=player)
    player.update_hero(playerhero, True)

    playerheroteam = player.heroteams.get(playerhero.warrior.hero.heroTeamId)
    playerheroteam.update_score()
    player.update_heroteam(playerheroteam, True)

    if player.tutorial_id == Static.TUTORIAL_ID_ADD_XP_12:
        player.tutorial_complete()

    for item_id, count in items.items():
        playeritem = player.items.get(item_id)
        playeritem.sub(count, info=info)

    return response


@handle_common
@require_player
def heroDecompose(request, response):
    """
    献祭
    """
    player = request.player
    # 包含主键数量的一个字典形式
    soul_ids = getattr(request.logic_request, "soulIds", [])

    info = u"献祭"

    soul_ids_len = len(soul_ids)

    soul_ids = dict(zip(soul_ids[0:soul_ids_len:2], soul_ids[1:soul_ids_len:2]))

    for pk, number in soul_ids.items():
        playersoul = player.souls.get(pk)
        if playersoul and playersoul.can_sub(number):
            soul = get_soul(pk)
            player.add_couragepoint(soul.couragePoint*number, info=info)
            player.add_gold(soul.gold*number, info=info)
            playersoul.sub(number, info=info)

    return response

@handle_common
@require_player
def heroCompose(request, response):
    """
    灵魂碎片合成英雄
    """
    player = request.player
    soul_id = getattr(request.logic_request, "soulId", 0)
    info = u"灵魂碎片合成英雄"

    soul = get_soul(soul_id)

    playersoul = player.souls.get(soul_id)
    if not playersoul or not playersoul.can_sub(soul.recruitCost):
        if not playersoul:
            player.delete_soul(soul_id)
        else:
            player.update_soul(playersoul)
        AlertHandler(player, response, AlertID.ALERT_HERO_COMPOSE_SOUL_NUMBER_NOT_ENOUGH, u"heroCompose:soul(%s) recruitCost(%s)" % (soul_id, soul.recruitCost))
        return response

    playerhero = player.heroes.get(soul.recruitHeroId)
    if playerhero:
        player.update_hero(playerhero)
        AlertHandler(player, response, AlertID.ALERT_HERO_ALREADY_EXSIT, u"heroCompose:soul(%s) recruitHeroId(%s) existed" % (soul_id, soul.recruitHeroId))
        return response

    playersoul.sub(soul.recruitCost, info=info)

    star = int(str(soul.warrior_id)[-2:])

    new_id = soul.warrior_id / 100 * 100

    acquire_hero(player, new_id, info=info, star=star)

    if player.tutorial_id == Static.TUTORIAL_ID_HEROCOMPOSE_10:
        player.tutorial_complete()
        player.next_tutorial_open()

    return response


@handle_common
@require_player
def heroUpgrade(request, response):
    """
    进阶
    """
    player = request.player
    playerhero_id = getattr(request.logic_request, "playerHeroId", 0)

    playerhero = player.heroes.get(playerhero_id)
    hero = playerhero.warrior.hero

    if playerhero.level < hero.evolveLevel:
        player.update_hero(playerhero)
        AlertHandler(player, response, AlertID.ALERT_HERO_UPGRADE_LEVEL_NOT_ENOUGH, u"evolveHero:hero(%s) playerhero(%s) level(%s) evolveLevel(%s)" % (playerhero.warrior_id, playerhero_id, playerhero.level , hero.evolveLevel))
        return response

    _warrior = get_warrior(hero.evolveHero_id)
    for cost in hero.evolveCosts:
        if not reward_cost_check(player, cost):
            AlertHandler(player, response, AlertID.ALERT_HERO_UPGRADE_MATERIAL_NOT_ENOUGH, u"evolveHero:hero(%s) playerhero(%s) cost(%s) is error" % (playerhero.warrior_id, playerhero_id, cost.pk))
            return response

    _info =u"进阶:%s,%s" % (playerhero.pk, playerhero.upgrade)

    for cost in hero.evolveCosts:
        reward_cost(player, cost)


    if _warrior.hero.is_purple:
        player.task_going(Static.TASK_CATEGORY_HERO_EVOLVE_UPGRADE_PURPLE, number=1, is_incr=True, is_series=True)
    elif _warrior.hero.is_blue:
        player.task_going(Static.TASK_CATEGORY_HERO_EVOLVE_UPGRADE_BLUE, number=1, is_incr=True, is_series=True)
        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_HERO_UPGRADE_BLUE, number=1, is_incr=True, is_series=True)
    elif _warrior.hero.is_green_plus_2:
        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_HERO_UPGRADE_GREEN2, number=1, is_incr=True, is_series=True)
    elif _warrior.hero.is_green_plus_1:
        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_HERO_UPGRADE_GREEN1, number=1, is_incr=True, is_series=True)
    if _warrior.hero.is_green:
        player.task_going(Static.TASK_CATEGORY_HERO_EVOLVE_UPGRADE_GREEN, number=1, is_incr=True, is_series=True)

    ActionLogWriter.hero_evolve(player, playerhero.pk, playerhero.warrior_id, _warrior.pk, playerhero.upgrade , _warrior.hero.upgrade, playerhero.warrior.cardId, _info)

    playerhero.warrior_id = _warrior.pk
    playerhero.upgrade = _warrior.hero.upgrade

    #检查是否开启新技能
    skillhero = get_heroskill(_warrior.cardId)
    for i in range(0, len(skillhero.skillinfo)/3):
        skillGild,_,upgrade = skillhero.skillinfo[i*3:(i+1)*3]
        if upgrade == playerhero.upgrade:
            setattr(playerhero, "skill%sLevel" %(i+1), 1)

    playerheroteam = player.heroteams.get(playerhero.warrior.hero.heroTeamId)
    playerheroteam.update_score()
    player.update_heroteam(playerheroteam, True)
    player.update_hero(playerhero, True)

    if player.tutorial_id == Static.TUTORIAL_ID_HERO_UPGRADE_15:
        player.tutorial_complete()

    return response


@handle_common
@require_player
def heroSkillLevelUp(request, response):
    """
    技能升级
    """
    player = request.player
    playerhero_id = getattr(request.logic_request, "playerHeroId", 0)
    skill_pos = getattr(request.logic_request, "pos", -1)
    playerhero = player.heroes.get(playerhero_id)

    if not playerhero:
        raise ErrorException(player, u"heroSkillLevelUp:no playerhero(%s)" % (playerhero_id))

    if not playerhero.skill_can_levelup(skill_pos):
        player.update_hero(playerhero)
        AlertHandler(player, response, AlertID.ALERT_HERO_SKILL_LEVELUP_ERROR, u"heroSkillLevelUp:hero(%s) playerhero(%s) pos(%s) can not levelup " % (playerhero.warrior_id, playerhero_id, skill_pos))
        return response

    if skill_pos <= 0 or skill_pos > 4:
        AlertHandler(player, response, AlertID.ALERT_HERO_SKILL_LEVELUP_ERROR, u"heroSkillLevelUp:hero(%s) playerhero(%s) pos(%s) " % (playerhero.warrior_id, playerhero_id, skill_pos))


    skill_id, skill_level = playerhero.get_skill_info(skill_pos)
    skilllevel = get_skilllevel(skill_id, skill_level)
    next_skilllevel = get_skilllevel(skill_id, skill_level+1)

    if not skilllevel:
        raise ErrorException(player, u"heroSkillLevelUp:hero(%s) playerhero(%s) skilllevel(%s)" % (playerhero.warrior_id, playerhero_id, skill_level))
    if not next_skilllevel:
        raise ErrorException(player, u"heroSkillLevelUp:hero(%s) playerhero(%s) nextskilllevel(%s)" % (playerhero.warrior_id, playerhero_id, skill_level+1))


    if playerhero.level < skilllevel.heroLevel:
        player.update_hero(playerhero)
        AlertHandler(player, response, AlertID.ALERT_HERO_SKILL_LEVELUP_LEVEL_NOT_ENOUGH, u"heroSkillLevelUp:hero(%s) playerhero(%s) level(%s) skilllevel(%s)" % (playerhero.warrior_id, playerhero_id, playerhero.level, skilllevel.heroLevel))
        return response

    _gold = skilllevel.costGold

    if player.gold < _gold:
        AlertHandler(player, response, AlertID.ALERT_GOLD_NOT_ENOUGH , u"heroSkillLevelUp:hero(%s) playerhero(%s) needGold(%s) playerGold(%s)" % (playerhero.warrior_id, playerhero_id, _gold, player.gold))
        return response

    for cost in skilllevel.costs:
        if not reward_cost_check(player, cost):
            AlertHandler(player, response, AlertID.ALERT_HERO_SKILL_LEVELUP_MATERIAL_NOT_ENOUGH, u"heroSkillLevelUp:hero(%s) playerhero(%s) cost(%s) is error" % (playerhero.warrior_id, playerhero_id, cost.pk))
            return response

    for cost in skilllevel.costs:
        reward_cost(player, cost)

    _info =u"技能升级:%s" % (playerhero.pk)
    player.sub_gold(_gold, _info)
    skill_id, before_level = playerhero.get_skill_info(skill_pos)
    playerhero.skill_levelup(skill_pos)
    _, after_level = playerhero.get_skill_info(skill_pos)
    ActionLogWriter.hero_skilllevelup(player, playerhero.pk, playerhero.warrior_id, skill_pos, skill_id, before_level, after_level, playerhero.warrior.cardId,_info)
    player.update_hero(playerhero, True)

    player.dailytask_going(Static.DAILYTASK_CATEGORY_HERO_LEVELUP, number=1, is_incr=True, is_series=True)

    if player.tutorial_id == Static.TUTORIAL_ID_SKILL_LEVELUP_13:
        player.tutorial_complete()

    return response

@handle_common
@require_player
def heroStarUpgrade(request, response):
    """
    英雄升星
    """
    # 获取升星英雄id
    playerhero_id = getattr(request.logic_request, "playerHeroId", 0)
    # 选择升星模式，是否优先使用英雄灵魂碎片，再使用万能碎片
    useSoulFirst = getattr(request.logic_request, "useSoulFirst", True)
    player = request.player

    playerhero = player.heroes.get(playerhero_id)

    if not playerhero:
        raise ErrorException(player, u"heroStarUpgrade:no playerhero(%s)" % (playerhero_id))

    # 通过英雄星级获取数据表中对应的数据
    herostarupgrade = get_herostarupgrade(playerhero.star)
    if not herostarupgrade:
        raise ErrorException(player, u"heroStarUpgrade:no herostarupgrade(%s)" % (playerhero.star))

    # 获取相应英雄的碎片
    soul_id = playerhero.warrior.hero.soulId
    playersoul = player.souls.get(soul_id)
    # 这个是英雄的碎片
    soul_number = playersoul.count if playersoul else 0
    soul_number = soul_number if soul_number <= herostarupgrade.soulCount else herostarupgrade.soulCount

    # 这个是万能的碎片
    player_soulitem = player.items.get(Static.ITEM_HERO_UPGRADE_ID)
    player_soulitem_number = player_soulitem.count if player_soulitem else 0
    soulitem_number = player_soulitem_number if player_soulitem_number < herostarupgrade.sepecialItemMaxCount else herostarupgrade.sepecialItemMaxCount

    # 但是使用有特殊的规则，万能碎片的使用数量有上限的限制，到达上限以后仍然不够的话需要使用英雄碎片补充。
    if soul_number + soulitem_number < herostarupgrade.soulCount:
        AlertHandler(player, response, AlertID.ALERT_SOUL_NOT_ENOUGH, u"heroStarUpgrade: playerheroId(%s) soulNumber(%s) soulitemNumber(%s) star(%s)" % (playerhero_id, soul_number, player_soulitem_number, playerhero.star))
        return response

    # 升星需要三种物品，英雄碎片，万能碎片，消耗表里面的物品。
    for cost in herostarupgrade.costs:
        if not reward_cost_check(player, cost):
            AlertHandler(player, response, AlertID.ALERT_HERO_STAR_UPGRADE_MATERIAL_NOT_ENOUGH, u"heroStarUpgrade: playerheroId(%s) cost(%s) is not enough star(%s)" % (playerhero_id, cost.id, playerhero.star))
            return response

    info = u"英雄(%s)升星(%s)" % (playerhero_id, playerhero.star)
    # 优先使用英雄灵魂碎片
    if useSoulFirst:
        playersoul.sub(soul_number, info)
        extra_soulitem_number = herostarupgrade.soulCount - soul_number
        if extra_soulitem_number > 0:
            player_soulitem.sub(extra_soulitem_number, info)
    else:
        if soulitem_number != 0:
            player_soulitem.sub(soulitem_number, info)
        extra_soul_number = herostarupgrade.soulCount - soulitem_number
        playersoul.sub(extra_soul_number, info)

    for cost in herostarupgrade.costs:
        reward_cost(player, cost)

    playerhero.start_upgrade()

    if playerhero.star == 3:
        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_HERO_STAR_UP_GREEN3, number=1, is_incr=True, is_series=True)

    elif playerhero.star == 5:
        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_HERO_STAR_UP_GREEN5, number=1, is_incr=True, is_series=True)

    elif playerhero.star == 6:
        player.task_going(Static.TASK_CATEGORY_HERO_STAR2_UPGRADE, number=1, is_incr=True, is_series=True)

    elif playerhero.star == 7:
        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_HERO_STAR_UP_BLUE2, number=1, is_incr=True, is_series=True)

    elif playerhero.star == 10:
        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_HERO_STAR_UP_BLUE5, number=1, is_incr=True, is_series=True)

    elif playerhero.star == 11:
        player.task_going(Static.TASK_CATEGORY_HERO_STAR3_UPGRADE, number=1, is_incr=True, is_series=True)
        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_HERO_STAR_UP_PURPLE, number=1, is_incr=True, is_series=True)

    elif playerhero.star == 16:
        player.task_going(Static.TASK_CATEGORY_HERO_STAR5_UPGRADE, number=1, is_incr=True, is_series=True)

    playerheroteam = player.heroteams.get(playerhero.warrior.hero.heroTeamId)
    playerheroteam.update_score()
    player.update_heroteam(playerheroteam, True)

    player.update_hero(playerhero, True)
    return response

@handle_common
@require_player
def heroDestiny(request, response):
    """
    英雄天命
    """
    playerhero_id = getattr(request.logic_request, "playerHeroId", 0)

    player = request.player

    playerhero = player.heroes.get(playerhero_id)
    if not playerhero:
        raise ErrorException(player, u"heroDestiny:playerhero(%s) is not existed" % (playerhero_id))

    # 根据天命等级或者数据表里面的数据
    herodestiny = get_herodestiny(playerhero.destinyLevel)
    if not herodestiny and playerhero.destinyLevel <= Static.HERO_DESTINY_LEVEL:
        raise ErrorException(player, u"heroDestiny:no herodestiny(%s)" % (playerhero.destinyLevel))

    # 英雄等级不够
    if playerhero.level < herodestiny.heroLevel:
        AlertHandler(player, response, AlertID.ALERT_LEVEL_NOT_ENOUGH, u"heroDestiny:playerhero(%s) herolevel(%s) < destinyHeroLevel(%s)" % (playerhero_id,  playerhero.level, herodestiny.heroLevel))
        return response

    # 取得现有所有天命石头，因为目前只有一种物品，以后如果有多种，更容易扩展
    item_id = Static.HERO_DESTINY_LIST[0]
    player_destinystone = player.items.get(item_id)
    if not player_destinystone:
        AlertHandler(player, response, AlertID.ALERT_ITEM_NOT_ENOUGH, u"heroDestiny:item_id(%s) number is not exits" % item_id)
        return response

    # 计算这些石头能够提供的所有经验
    player_destinystonexp = player_destinystone.count * player_destinystone.item.number

    #提供的经验不够
    if playerhero.destinyLevel <= Static.HERO_DESTINY_LEVEL:
        if player_destinystonexp < herodestiny.stoneCost:
            AlertHandler(player, response, AlertID.ALERT_ITEM_NOT_ENOUGH, u"heroDestiny:item_id(%s) number is not enough" % item_id)
            return response
        else:
            cost_count = herodestiny.stoneCost/player_destinystone.item.number
    else:
        if player_destinystonexp < playerhero.destinyLevel * Static.HERO_DESTINY_COST_RATIO:
            AlertHandler(player, response, AlertID.ALERT_ITEM_NOT_ENOUGH, u"heroDestiny:item_id(%s) number is not enough" % item_id)
            return response
        else:
            cost_count = playerhero.destinyLevel * Static.HERO_DESTINY_COST_RATIO/player_destinystone.item.number

    info = u"英雄天命:%s" % playerhero_id

    #进行天命
    playerhero.destiny()
    if playerhero.destinyLevel == 1:
        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_HERO_DESTINY_LEVEL1, number=1, is_incr=True,with_top=False, is_series=True)
    if playerhero.destinyLevel == 3:
        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_HERO_DESTINY_LEVEL3, number=1, is_incr=True,with_top=False, is_series=True)
    elif playerhero.destinyLevel == 5:
        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_HERO_DESTINY_LEVEL5, number=1, is_incr=True,with_top=False, is_series=True)

    player_destinystone.sub(cost_count, info=info)
    player.update_hero(playerhero, True)
    return response

# @handle_common
# @require_player
# def heroTrain(request, response):
#     """
#     英雄培养
#     """
#     playerhero_id = getattr(request.logic_request, "playerHeroId", 0)
#     train_type = getattr(request.logic_request, "trainType", 0)
#     # 培养次数
#     count = getattr(request.logic_request, "count", 0)

#     player = request.player

#     playerhero = player.heroes.get(playerhero_id)

#     if not playerhero:
#         raise ErrorException(player, u"heroTrain:playerhero(%s) is not existed" % (playerhero_id))

#     if count >= 10 and player.vip_level < 8:
#         AlertHandler(player, response, AlertID.ALERT_PLAYER_VIP_LEVEL_NOT_ENOUGH, u"heroTrain:VIPlevel needs(%s) now is  (%s) " % (8, player.vip_level))
#         return response
#     elif count >= 5 and player.vip_level < 4:
#         AlertHandler(player, response, AlertID.ALERT_PLAYER_VIP_LEVEL_NOT_ENOUGH, u"heroTrain:VIPlevel needs(%s) now is  (%s) " % (4, player.vip_level))
#         return response
#     else:
#         pass

#     # 培养表里面的主键就是英雄的cardId
#     train_id = playerhero.warrior.cardId
#     herotrain = get_herotrain(train_id)
#     if not herotrain:
#         raise ErrorException(player, u"heroTrain:train_id(%s) is not existed" % (train_id))

#     playeritem = player.items.get(Static.ITEM_TRAIN_ID)

#     if not playeritem:
#          AlertHandler(player, response, AlertID.ALERT_ITEM_NOT_ENOUGH,  u"heroTrain:playeritem(%s)" % (Static.ITEM_TRAIN_ID))
#          return response

#     if not playeritem.can_sub(herotrain.count * count):
#         AlertHandler(player, response, AlertID.ALERT_ITEM_NOT_ENOUGH,  u"heroTrain:playeritem(%s) useCount(%s) count(%s)" % (Static.ITEM_TRAIN_ID, herotrain.count * count, playeritem.count))
#         return response

#     # 培养有三种方式，1 代表培养丹 2 代表培养丹加金币 3 代表培养丹加钻石
#     if train_type == 2 and player.gold < herotrain.goldCost * count:
#         AlertHandler(player, response, AlertID.ALERT_ITEM_NOT_ENOUGH,  u"heroTrain: playergold(%s) <  count(%s)" % (player.gold, herotrain.goldCost * count))
#         return response
#     elif train_type == 3 and player.yuanbo < herotrain.diamondCost * count:
#         AlertHandler(player, response, AlertID.ALERT_ITEM_NOT_ENOUGH,  u"heroTrain: playeryuanbo(%s) <  count(%s)" % (player.yuanbo, herotrain.diamondCost * count))
#         return response

#     info = u"英雄培养(%s)" % playerhero_id
#     # 扣除物品

#     playeritem.sub(herotrain.count * count, info=info)
#     if train_type == 2:
#         player.sub_gold(herotrain.goldCost * count, info=info)
#     elif train_type == 3:
#         player.sub_yuanbo(herotrain.diamondCost * count, info=info)

#     player.dailytask_going(Static.DAILYTASK_CATEGORY_TRAIN, number=1, is_incr=True, is_series=True)


#     playerhero.train(train_type, herotrain, count)
#     player.update_hero(playerhero, True)


#     return response

# @handle_common
# @require_player
# def heroTrainConfirm(request, response):
#     """
#     英雄培养确认
#     """

#     player = request.player
#     playerhero_id = getattr(request.logic_request, "playerHeroId", 0)
#     playerhero = player.heroes.get(playerhero_id)

#     if not playerhero:
#         raise ErrorException(player, u"heroTrain:playerhero(%s) is not existed" % (playerhero_id))

#     playerhero.train_confirm()
#     player.update_hero(playerhero, True)

#     return response

# @handle_common
# @require_player
# def heroTeamLevelUp(request, response):
#     """
#     英雄组队升级
#     """

#     player = request.player
#     team_id = getattr(request.logic_request, "teamId", 0)
#     playerheroteam = player.heroteams.get(team_id)

#     # 根据id，level可以获得组队的信息。
#     heroteamlevel = get_heroteamlevel_by_teamid_level(team_id, playerheroteam.level)
#     # 取得下一个级别的组队信息
#     heroteamnextlevel = get_heroteamlevel(heroteamlevel.nextLevelId)

#     if not heroteamlevel:
#         raise ErrorException(player, u"heroTeamLevelUp:heroteamlevel(%s) is not existed" % (team_id * 1000 + playerheroteam.level))

#     # 如果没有下一个级别，那么当前就是顶级了
#     if not heroteamnextlevel:
#         AlertHandler(player, response, AlertID.ALERT_HEROTEAM_LEVEL_IS_MAX,  u"heroTeamLevelUp:heroteamlevel(%s)" % (team_id * 1000 + playerheroteam.level))
#         return response

#     # 组队的天命等级不能大于玩家的等级
#     if heroteamnextlevel.level > player.level:
#         AlertHandler(player, response, AlertID.ALERT_PLAYER_LEVEL_NOT_ENOUGH,  u"heroTeamLevelUp:heroteamnextlevel needs(%s) > playerlevel(%s))" % (heroteamnextlevel.level, player.level))
#         return response

#     info = "英雄组队升级:%s" % team_id

#     for cost in heroteamlevel.costs:
#         if not reward_cost_check(player, cost):
#             AlertHandler(player, response, AlertID.ALERT_GOLD_NOT_ENOUGH,  u"heroTeamLevelUp:playeritem(%s)" % (cost.type))
#             return response

#     # 组队的分数不足，不可以升级
#     if playerheroteam.score < heroteamlevel.score:
#         AlertHandler(player, response, AlertID.ALERT_SCORE_NOT_ENOUGH,  u"heroTeamLevelUp: playerheroteamscore(%s) <  heroteamlevelscore(%s)" % (playerheroteam.score, heroteamlevel.score))
#         return response
    
#     for cost in heroteamlevel.costs:
#         reward_cost(player, cost, info=info)

#     playerheroteam.level_up(heroteamnextlevel)
#     player.update_heroteam(playerheroteam, True)

#     return response

@handle_common
@require_player
def debugGetAllHeroes(request, response):
    """
    英雄组队升级

    """

    player = request.player
    items = get_items()
    equips = get_equips()
    equipsfras = get_equipfragments()
    arts = get_artifacts()
    artfras = get_artifactfragments()
    souls = get_souls()
    for item in items:
        acquire_item(player, item, 10000)
    for equip in equips:
        acquire_equip(player, equip, 10000)
    for eqfa in equipsfras:
        acquire_equipfragment(player, eqfa, 10000)
    for art in arts:
        acquire_artifact(player, art, 10000)
    for artfa in artfras:
        acquire_artifactfragment(player, artfa, 10000)
    for soul in souls:
        acquire_soul(player, soul, 10000)
    playerheroes = player.heroes.all().keys()
    for hero in playerheroes:
        player.heroes.delete(hero)

    acquire_hero(player, 111000109, level=30, star=5, upgrade = 9)
    acquire_hero(player, 111000209, level=30, star=5, upgrade = 9)
    acquire_hero(player, 111000309, level=30, star=5, upgrade = 9)
    acquire_hero(player, 111000509, level=30, star=5, upgrade = 9)
    acquire_hero(player, 113000309, level=30, star=5, upgrade = 9)
    acquire_hero(player, 112000209, level=30, star=5, upgrade = 9)
    acquire_hero(player, 112000409, level=30, star=5, upgrade = 9)
    acquire_hero(player, 112000509, level=30, star=5, upgrade = 9)
    acquire_hero(player, 112000609, level=30, star=5, upgrade = 9)
    acquire_hero(player, 112000709, level=30, star=5, upgrade = 9)
    acquire_hero(player, 113000109, level=30, star=5, upgrade = 9)
    acquire_hero(player, 114000209, level=30, star=5, upgrade = 9)
    acquire_hero(player, 114000309, level=30, star=5, upgrade = 9)
    acquire_hero(player, 114000409, level=30, star=5, upgrade = 9)
    acquire_hero(player, 114000509, level=30, star=5, upgrade = 9)
    acquire_hero(player, 114000609, level=30, star=5, upgrade = 9)
    acquire_hero(player, 115000209, level=30, star=5, upgrade = 9)
    acquire_hero(player, 115000309, level=30, star=5, upgrade = 9)
    acquire_hero(player, 115000509, level=30, star=5, upgrade = 9)
    acquire_hero(player, 116000109, level=30, star=5, upgrade = 9)
    acquire_hero(player, 116000209, level=30, star=5, upgrade = 9)
    acquire_hero(player, 116000309, level=30, star=5, upgrade = 9)
    acquire_hero(player, 116000409, level=30, star=5, upgrade = 9)
    acquire_hero(player, 116000509, level=30, star=5, upgrade = 9)
    acquire_hero(player, 114000709, level=30, star=5, upgrade = 9)
    acquire_hero(player, 116000709, level=30, star=5, upgrade = 9)
    acquire_hero(player, 112000809, level=30, star=5, upgrade = 9)

    return response







