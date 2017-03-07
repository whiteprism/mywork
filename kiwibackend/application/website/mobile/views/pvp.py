# -*- encoding:utf-8 -*-
from decorators import require_player, handle_common
from module.common.static import Static, AlertID
from module.player.api import get_player, filter_robots_by_level, get_pvp_players
from module.playerPVP.api import pvp_fight
from module.common.middleware import ErrorException, AlertHandler
from module.playerequip.api import get_playerheroes_equips, acquire_equip, acquire_equipfragment
from module.playerartifact.api import get_playerheroes_artifacts, acquire_artifactfragment
from module.playerPVP.docs import PVPRank
from module.artifact.api import get_artifactfragment, get_artifact
import random, datetime, time
from module.mail.api import send_attack_mail, send_defense_mail
from module.battlerecords.api import send_battle_record, get_records
from module.vip.api import get_vip
from module.playersoul.api import acquire_soul
from module.playeritem.api import acquire_item
from module.playerplayback.api import get_warrior_and_tech_dict_list_by_army_data
import math
from utils import random_item_pick
from module.gashapon.api import get_gashapon

@handle_common
@require_player
def pvpSetUp(request, response):
    '''
    PVP阵容
    '''
    player = request.player
    # 这个是选中敌人的id
    target_player_id = getattr(request.logic_request, "oppId", 0)
    category = getattr(request.logic_request, "category", 0) # 1竞技场 2掠夺 3攻城战
    target_player = get_player(target_player_id, False)
    
    #竞技场
    if category == 1:
        #竞技场未开放
        if not player.isOpenArena:
            AlertHandler(player,response, AlertID.ALERT_LEVEL_SHORTAGE, u"pvpSetUp:PVP playerLevel(%s)" % (player.level))
            return response

        #耐力不足
        if player.stamina < Static.PVP_SUB_STAMINA:
            AlertHandler(player,  response, AlertID.ALERT_STAMINA_NOT_ENOUGH, u"pvpSetUp:stamina not enougth")
            return response
        now = datetime.datetime.now()
        week = now.isoweekday()
        hour = now.hour
        if week == Static.PVP_STOP_WEEK and hour < Static.PVP_STOP_HOUR:
            response.logic_response.set("openState", 2)
            return
        # 是否达到冷却时间。
        # 从django里面取出来的时间类型是带有时区的复杂类型。所以需要将时区的信息去除掉。这样才能和正常的日期类型去做比较
        player.PVP.cd_time = player.PVP.cd_time.replace(tzinfo=None)
        if player.PVP.cd_time > datetime.datetime.now():
            return response

        # 每日战斗五次
        if player.PVP.freeBattleCount <= 0:
            return response
        player.sub_stamina(Static.PVP_SUB_STAMINA)
        #　扣除耐力
        # 之所以放在请求战斗里面去做，主要是因为怕玩家中途杀掉进程，可以逃避扣除耐力的做法
        player.PVP.subBattleCount()
        player.PVP.update()
        #PVP 战斗一次
        player.dailytask_going(Static.DAILYTASK_CATEGORY_PK, number=1, is_incr=True, is_series=True)

        playback_data = {}
        #竞技场

        playback_data = {"leftArmyData": target_player.army_data}
        response.logic_response.set("playback", playback_data)
        response.logic_response.set("category", category)
        response.logic_response.set("openState", 1)
        # 场景目前是表里面配置了三十二个。如果以后表里面有修改，
        response.logic_response.set("pvpSceneId", random.randint(1, 7) * 10)
    elif category == 3:
        #耐力不足
        if target_player_id != -10001:
            #攻城战未开放
            if not player.isOpenSiege:
                AlertHandler(player,response, AlertID.ALERT_LEVEL_SHORTAGE, u"pvpSetUp:siege playerLevel(%s)" % (player.level))
                return response
            if player.stamina < Static.SIEGE_SUB_STAMINA:
                AlertHandler(player, response, AlertID.ALERT_STAMINA_NOT_ENOUGH, u"pvpSetUp:stamina not enougth")
                return response

            if player.SiegeBattle.isInCDTime or not player.SiegeBattle.canBattle:
                return response

            opp = player.SiegeBattle.get_opp(target_player_id)

            if not opp:
                response.common_response.player.set("siegeBattle", player.SiegeBattle.to_dict())
                AlertHandler(player, response, AlertID.ALERT_SIEGE_BATTLE_PLAYER_IS_REFRESH, u"pvpSetUp: is refresh")
                return response

            # if target_player.siegeBattle_isLock:
            #     AlertHandler(player, response, AlertID.ALERT_SIEGE_BATTLE_PLAYER_IN_WARAVOID, u"pvpSetUp: in waravoid")
            #     return response

            if target_player.is_onLine:
                AlertHandler(player, response, AlertID.ALERT_SIEGE_BATTLE_PLAYER_ONLINE, u"pvpSetUp: is online")
                return response

            if target_player.guildId > 0 and target_player.guildId == player.guildId:
                AlertHandler(player, response, AlertID.ALERT_SIEGE_BATTLE_PLAYER_SAME_GUILD, u"pvpSetUp: samle guild")
                return response

            player.sub_stamina(Static.SIEGE_SUB_STAMINA)
            player.SiegeBattle.set_pkOpp(opp)
            response.common_response.player.set("siegeBattle", player.SiegeBattle.to_dict())

        playback_data = {"leftArmyData": target_player.building_army_data}
        response.logic_response.set("playback", playback_data)
        response.logic_response.set("category", category)
        response.logic_response.set("openState", 1)
        response.logic_response.set("pvpSceneId", random.randint(1, 7) * 10)

    return response


@handle_common
@require_player
def pvpOpps(request, response):

    '''
    pvp 列表
    '''
    player = request.player
    #玩家没有到达PVP建筑开启等级
    if not player.isOpenArena:
        #　在前端提示弹窗，如果想加一个新的，格式就是这么写，在Static.py里面定义一个常量。然后告诉策划这个常量代表什么意思
        AlertHandler(player,  response, AlertID.ALERT_LEVEL_SHORTAGE, u"pvpOpps:playerLevel(%s) startLevel(%s)" % (player.level, Static.PVP_LEVEL))
        return response

    #竞技场每周一0点至8点关闭
    now = datetime.datetime.now()
    week = now.isoweekday()
    hour = now.hour
    if week == Static.PVP_STOP_WEEK and hour < Static.PVP_STOP_HOUR:
        response.logic_response.set("openState", 2)
        return response

    # 这里至少是5个人.
    opp_ids = player.PVP.get_oppIds()
    sumOpps = []
    new_oppids = random.sample(opp_ids, 5)
    opps = get_pvp_players(new_oppids)

    for opp in opps:
        sumOpps.append(opp.pvp_view_data(True))

    response.common_response.player.set("opps", sumOpps)

    response.common_response.player.set("arena", player.PVP.to_dict())

    response.logic_response.set("openState", 1)

    return response

@handle_common
@require_player
def pvpCDTimeDelete(request, response):

    '''
    pvp 清除冷却时间
    '''

    # 在冷却的时间内不能进行战斗也不能进行刷新对手。如果想要做上述操作，需要先清除冷却的cd
    player = request.player

    #玩家没有到达PVP建筑开启等级
    if not player.isOpenArena:
        AlertHandler(player, response, AlertID.ALERT_LEVEL_SHORTAGE, u"pvpCDTimeDelete:playerLevel(%s) startLevel(%s)" % (player.level, Static.PVP_LEVEL))
        return response

    if player.yuanbo < Static.PVP_DELETE_CD_TIME_COST:
        AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"pvpCDTimeDelete cost(%s) now player have (%s)" % (Static.PVP_DELETE_CD_TIME_COST, player.yuanbo))
        return response

    player.PVP.cd_time = datetime.datetime.now()
    player.PVP.update()
    player.sub_yuanbo(Static.PVP_DELETE_CD_TIME_COST,info=u"清除PVP冷却时间")

    response.common_response.player.set("arena", player.PVP.to_dict())

    return response


@handle_common
@require_player
def pvpResetCount(request, response):

    '''
    pvp
    '''
    player = request.player

    #玩家没有到达PVP建筑开启等级
    if not player.isOpenArena:
        AlertHandler(player, response, AlertID.ALERT_LEVEL_SHORTAGE, u"pvpOpps:playerLevel(%s) startLevel(%s)" % (player.level, Static.PVP_LEVEL))
        return response

    vip = get_vip(player.vip_level)

    if player.PVP.resetCount >= vip.resetPVPCount:
        AlertHandler(player, response, AlertID.ALERT_RESET_PVP_COUNT_NOT_ENOUGH, u"pvpResetCount:player pvpResetCount(%s) >= now VIP can have (%s)" % (player.PVP.resetCount, vip.resetPVPCount))
    needDiamond = player.PVP.resetCost

    if player.yuanbo < needDiamond:
        AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"pvpResetCount:player has (%s) reset PVP need (%s)" % (player.yuanbo, needDiamond))
        return response

    player.PVP.resetPVPCount()
    player.sub_yuanbo(needDiamond, info=u"竞技场重置")
    response.common_response.player.set("arena", player.PVP.to_dict())

    return response

@handle_common
@require_player
def pvpStart(request, response):
    '''
    PVP结算
    '''
    pvpType = getattr(request.logic_request, "pvpType", 0) #战斗力

    #竞技场
    if pvpType == 1:
        return _pvpBattleResult(request, response)
    #攻城战
    elif pvpType == 3:
        return _siegeBattleResult(request, response)

def _pvpBattleResult(request, response):
    """
    竞技场
    """
    player = request.player
    target_player_id = getattr(request.logic_request, "oppId", 0)
    playback = getattr(request.logic_request, "playback", [])
    layout = getattr(request.logic_request, "layout", [])
    isWin = getattr(request.logic_request, "isWin", 0)
    summary = getattr(request.logic_request, "summary", 0) #死亡情况
    powerrank = getattr(request.logic_request, "powerRank", 0) #战斗力
    now = datetime.datetime.now()
    hour = now.hour

    # 未达到竞技场等级。
    if not player.isOpenArena:
        AlertHandler(player,response, AlertID.ALERT_LEVEL_SHORTAGE, u"_pvpBattleResult:playerLevel(%s) startLevel(%s)" % (player.level, Static.PVP_LEVEL))

    # 未到竞技场开启时间
    week = now.isoweekday()
    if week == Static.PVP_STOP_WEEK and hour < Static.PVP_STOP_HOUR:
        response.logic_response.set("openState", 2)
        return response

    player.update_hero_layout(layout)
    target_player = get_player(target_player_id, False)

    # 验证是否有对面的玩家。
    if not target_player:
        raise ErrorException(player, u"_pvpBattleResult:pvp target player is None:target player id(%s) is not existed" % target_player_id)
    rewards = pvp_fight(player, target_player, isWin)

    if isWin:
        player.task_going(Static.TASK_CATEGORY_ARENA_PK_SUCCESS, is_incr=True)

    score = 0

    for reward in rewards:
        if reward["type"] == Static.SCORE_ID:
            score = reward["count"]

    # pvp 的分支,pvp已经没有邮件的功能了。改成战斗记录的操作了。
    send_battle_record(player=player, isWin=isWin, playerScore=player.PVP.score, playerRank=player.PVP.rank, targetPlayerScore=target_player.PVP.score, targetPlayerRank=target_player.PVP.rank, addScore=score,playerPowerRank = player.powerRank, targetPlayerId=target_player.pk,targetPlayerPowerRank=target_player.powerRank, playerVip=int(player.vip_level), playerIcon=player.iconId, targetPlayerVip=int(target_player.vip_level), targetPlayerIcon=target_player.iconId)

    # 竞技场排名七天乐奖励
    rank = 1000 - player.PVP.rank
    rank = rank if rank > 0 else 0
    player.seven_days_task_going(category=Static.SEVEN_TASK_CATEGORY_PVP_RANK, number=rank, is_incr=False, with_top=True, is_series=True)

    player.PVP.update_oppIds()

    ## 这里至少是5个人.
    opp_ids = player.PVP.get_oppIds()
    sumOpps = []
    new_oppids = random.sample(opp_ids, 5)
    opps = get_pvp_players(new_oppids)
    for opp in opps:
        sumOpps.append(opp.pvp_view_data(True))
    response.common_response.player.set("opps", sumOpps)

    #战斗失败添加冷却时间
    if not isWin:
        player.PVP.updateCdTime()

    player.PVP.update()

    target_player.PVP.update()

    response.common_response.player.set("arena", player.PVP.to_dict())

    response.logic_response.set("heroLevelUp", [])
    response.logic_response.set("oppName", target_player.name)
    response.logic_response.set("rewards", rewards)
    response.logic_response.set("openState", 1)

    return response

def _siegeBattleResult(request, response):
    """
    攻城战结算
    """
    # 发起攻击的一方
    player = request.player
    # 防守的一方
    target_player_id = getattr(request.logic_request, "oppId", 0)
    playback = getattr(request.logic_request, "playback", [])
    fortIndexes = getattr(request.logic_request, "fortIndexes", []) #运输堡垒使用
    target_player = get_player(target_player_id)

    # 输了的玩家会在一段启动保护机制，不会在一段时间内 被其他玩家搜索到，这样通过锁定时间可以将这个时间 设置的长一些。
    # 输的玩家只会在输掉以后损失相应的金币和木材。不会损失其他东西。
    # 发起攻击的一方 需要消耗一种新的点数。每发起一次攻击扣除一点。
    # 所有扣除东西在结算的接口去做
    isWin = getattr(request.logic_request, "isWin", False)
    # 先结算防守方丢失
    rewards = []
    defence_rewards = []

    if not player.isOpenSiege:
        AlertHandler(player,response, AlertID.ALERT_LEVEL_SHORTAGE, u"_siegeBattleResult:playerLevel(%s) startLevel(%s)" % (player.level, Static.SIEGE_LEVEL))
        return response

    if not player.SiegeBattle.canBattle:
        return response

    leftArmyData = playback["leftArmyData"]
    heroInfos, _ = get_warrior_and_tech_dict_list_by_army_data(leftArmyData)

    #最多5个
    if len(heroInfos) + len(fortIndexes) > 5:
        return response

    opp =  player.SiegeBattle.pkOpp

    player.SiegeBattle.replaceOpp()
    fortUseNumber = 0
    fortInfos = player.SiegeBattle.fortInfos
    for fortIndex in fortIndexes:
        if fortInfos[fortIndex - 1] == 0:
            fortUseNumber += 1
    player.SiegeBattle.forts_use(fortIndexes)
    player.set_lock_time(0) #攻击敌人保护取消
    
    if isWin:
        ratioPercent = Static.SIEGE_BASE_PVP_RATIO * len(heroInfos)  + Static.SIEGE_FORT_PVP_RATIO * fortUseNumber
        baseRewards = opp["rewards"]
        winGold = 0
        winMaxGold = 0
        winWood = 0
        winMaxWood = 0
        lostGold = 0
        lostWood = 0
        for baseReward in baseRewards:
            if baseReward["type"] == Static.GOLD_ID:
                winGold = int(baseReward["count"] * ratioPercent)
                winMaxGold = baseReward["count"]

            if baseReward["type"] == Static.WOOD_ID:
                winWood = int(baseReward["count"] * ratioPercent)
                winMaxWood = baseReward["count"]

            rewards.append({
                "type":baseReward["type"],
                "count": int(baseReward["count"] * ratioPercent)
            })

        rewards.append({"type": Static.ITEM_HERO_UPGRADE_ID, "count": 1,})

        if fortUseNumber > 0:
            gashapon = get_gashapon(Static.SIEGE_REWARD_GASHAPON_ID)
            is_new, playergashapon = player.gashapons.get_or_create(gashapon.pk)
            units = playergashapon.acquire(player, gashapon, count=fortUseNumber)
            for unit in units:
                tmpReward = {"count":unit.gashapon_number, "type": unit.obj_id}
                rewards.append(tmpReward)


        if target_player.id > 0:
            lostMaxGold = target_player.gold if target_player.gold  < winMaxGold else winMaxGold 
            lostMaxWood = target_player.wood if target_player.wood  < winMaxWood else winMaxWood
            lostGold = int(lostMaxGold * ratioPercent * (1 - target_player.siege_proected))
            defence_rewards.append({"type":Static.GOLD_ID, "count":lostGold})
            lostWood = int(lostMaxWood * ratioPercent * (1 - target_player.siege_proected))
            defence_rewards.append({"type":Static.WOOD_ID, "count":lostWood})

            # 设置保护时间
            target_player.lost_siegebattle_result(lostGold, lostWood)
            target_player.set_lock_time(1)#dbug
            #target_player.set_lock_time(3600)#
            target_player.passive_update()

        # 万能碎片一个
        acquire_item(player, Static.ITEM_HERO_UPGRADE_ID, 1, info=u"攻城战胜利所得")
        player.win_siegebattle_result(winGold, winWood)
        player.SiegeBattle.add_winCount()
        player.task_going(Static.TASK_CATEGORY_SIEGE_TOTAL_COUNT, number=player.SiegeBattle.winCount, is_incr=False, is_series=True)

        #邮件部分
        content_attack  = "fytext_300712"
        params_attack = [str(target_player.name), str(winGold), str(winWood)]
        content_defense = "fytext_300714"
        params_defense = [str(player.name), str(lostGold), str(lostWood)]
    else:
        #添加CD时间
        player.SiegeBattle.set_cdTime()
        #邮件部分
        content_attack = "fytext_300713"
        params_attack = [str(target_player.name)]
        content_defense = "fytext_300715"
        params_defense = [str(player.name)]


    player.SiegeBattle.use_battleTimes()

    content_attacks = []
    content_attacks.append({
        "content": content_attack,
        "paramList": params_attack,
    })

    content_defenses = []
    content_defenses.append({
        "content": content_defense,
        "paramList": params_defense,
    })

    send_attack_mail(player, target_player, title="fytext_300728", contents=content_attacks, playback=playback, isWin=isWin, mailType=1, rewards=rewards)
    if target_player.id > 0:
        send_defense_mail(target_player, player, title="fytext_300728", contents=content_defenses, playback=playback, isWin=isWin, mailType=1, rewards=rewards)

    player.SiegeBattle.update()


    response.logic_response.set("rewards", rewards)

    response.common_response.player.set("siegeBattle", player.SiegeBattle.to_dict())
    return response

@handle_common
@require_player
def pvpRank(request, response):
    '''
    PVP世界排名
    '''
    player = request.player
    now = datetime.datetime.now()
    week = now.isoweekday()
    hour = now.hour
    #  这个字段表明　是否需要上周的数据
    last_rank = False

    # 如果当前是不允许ｐｖｐ战斗的时间，取得的数据上周的排行。
    if week == Static.PVP_STOP_WEEK and hour < Static.PVP_STOP_HOUR:
        last_rank = True
        rank_datas = PVPRank.get_last_ranks()
    else:
        rank_datas = PVPRank.get_ranks()
    opp_data = []
    for p_id, p_score in rank_datas:
        if not p_id or p_id == "None":
            continue
        if p_score >= Static.PVP_INIT_SCORE:
            opp_player = get_player(p_id, False)
            if opp_player and opp_player.level >= Static.PVP_LEVEL:
                dicts = opp_player.pvp_view_data(can_fight=True, last_rank=last_rank)
                opp_data.append(dicts)

    response.logic_response.set("rankOpps", opp_data)
    return response

@handle_common
@require_player
def pvpEnemyData(request, response):
    '''
    敌军 详细数据
    '''
    player = request.player
    target_player_id = getattr(request.logic_request, "userId", 0)
    target_player = get_player(target_player_id, False)
    if not target_player:
        raise ErrorException(player, u"pvpEnemyData:pvp army layout target player is None:target player id(%s) is not existed" % target_player_id)

    all_heros = target_player.layoutSiegeHeroes
    artifacts_view_list = []
    equips_view_list = []
    hero_view_list = []
    for hero in all_heros:
        hero_view_list.append(hero.to_dict())
        all_hero_equips = get_playerheroes_equips(target_player, [hero])
        for equip in all_hero_equips:
            equips_view_list.append(equip.to_dict())
        all_hero_artifacts = get_playerheroes_artifacts(target_player, [hero])
        for artifact in all_hero_artifacts:
            artifacts_view_list.append(artifact.to_dict())
    response.logic_response.set("artifacts", artifacts_view_list)
    response.logic_response.set("equips", equips_view_list)
    response.logic_response.set("heros", hero_view_list)
    response.logic_response.set("user", target_player.userSimple_dict())

    return response

@handle_common
@require_player
def pvpDefenseArmy(request, response):
    """
    设置防守阵容
    """
    # playback_data = {}
    player = request.player
    category = getattr(request.logic_request, "category", 0) # 1,竞技场 2,攻城战英雄 3,攻城战英雄
    defenseLayout = getattr(request.logic_request, "heroLayoutData", [])
    defenseList = []
    default_poses = Static.HERO_DEFENCE_POS
    i = 0
    for defenseheroid in defenseLayout[0:5]:
        defenseList.append(defenseheroid)
        defenseList.append(default_poses[i])
        i += 1
    if category == 1:
        #竞技场的防守阵容
        defenseHeroIds = []
        player.defenseHeroLayout = defenseList
        player.update_hero_defenseLayout(defenseList)
        defenseHeroIds = player.defenseHeroLayout[0:len(player.defenseHeroLayout):2]
        player.defenseHeroIds = defenseHeroIds
        player.update_hero_defenseHeroIds(defenseHeroIds)
        response.common_response.player.set("defenseHeroIds", defenseHeroIds)
        response.logic_response.set("state", 1)
    elif category == 2:
        #攻城战英雄的防守阵容
        defenseSiegeIds = []
        player.update_siege_defenseLayout(defenseList)
        defenseSiegeIds = defenseList[0:len(player.defenseSiegeLayout):2]
        player.update_siege_defenseHeroIds(defenseSiegeIds)
        response.common_response.player.set("defenseSiegeIds", defenseSiegeIds)
    elif category == 3:
        #攻城战士兵的防守阵容
        if len(defenseLayout) != len(player.defenseSiegeSoldierIds):
            raise ErrorException(player, u"pvpDefenseArmy:pvp defense layout is incorrect: layout is %s" % str(defenseLayout))

        player.update_siege_defenseSoldierIds(defenseLayout)
        response.common_response.player.set("defenseSiegeSoldierIds", defenseLayout)
    return response

@handle_common
@require_player
def siegeBattlePlayer(request, response):
    """
    搜索攻城战对手
    """

    player = request.player

    # 检查等级
    if not player.isOpenSiege:
        AlertHandler(player, response, AlertID.ALERT_PLAYER_LEVEL_NOT_ENOUGH, u"siegeBattlePlayer:need level(%s) player level is %s" %(Static.SIEGE_LEVEL, player.level))
        return response

    #如果为非自动刷新
    if player.SiegeBattle.refresh_auto():
        pass
    else:
        lockCount = player.SiegeBattle.oppsLockCount
        #5个对手都锁住则不刷新
        if lockCount == 5:
            response.common_response.player.set("siegeBattle", player.SiegeBattle.to_dict())
            return response 

        costGold = Static.SIEGE_REFRESH_COST_GOLD * (lockCount + 1)
        #金币不足
        if player.gold < costGold: 
            AlertHandler(player, response, AlertID.ALERT_GOLD_NOT_ENOUGH, u"siegeBattlePlayer:refresh cost(%s) playerGold(%s)" % (costGold, player.gold))
            return response
        player.sub_gold(costGold, u"搜索攻城战对手")
        player.SiegeBattle.refresh()

    response.common_response.player.set("siegeBattle", player.SiegeBattle.to_dict())
    return response

@handle_common
@require_player
def siegeBattlePlayerLock(request, response):
    """
    攻城战对手锁定 or 解锁
    """

    player = request.player
    oppId = getattr(request.logic_request, "oppId", 0)
    isLocked = True
    # 检查等级
    if not player.isOpenSiege:
        AlertHandler(player, response, AlertID.ALERT_PLAYER_LEVEL_NOT_ENOUGH, u"siegeBattlePlayerLock:need level(%s) player level is %s" %(Static.SIEGE_LEVEL, player.level))
        return response

    for _index, _opp in enumerate(player.SiegeBattle.opps):
        _player = get_player(_opp["player_id"], False)

        if _opp["player_id"] == oppId:
            player.SiegeBattle.opps[_index]["isLocked"] = not _opp["isLocked"]
            player.SiegeBattle.update()
            isLocked = player.SiegeBattle.opps[_index]["isLocked"]
            break

    response.logic_response.set("isLocked", isLocked)
    response.common_response.player.set("siegeBattle", player.SiegeBattle.to_dict())
    return response

@handle_common
@require_player
def siegeBattleDelCDTime(request, response):
    """
    攻城战删除冷却时间
    """

    player = request.player
    # 检查等级
    if not player.isOpenSiege:
        AlertHandler(player, response, AlertID.ALERT_PLAYER_LEVEL_NOT_ENOUGH, u"siegeBattleDelCDTime:need level(%s) player level is %s" %(Static.SIEGE_LEVEL, player.level))
        return response
    if player.yuanbo < Static.SIEGE_DELETE_CD_TIME_COST:
        AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"siegeBattleDelCDTime cost(%s) now player have (%s)" % (Static.SIEGE_DELETE_CD_TIME_COST, player.yuanbo))
        return response

    player.SiegeBattle.reset_cdTime()
    player.SiegeBattle.update()
    player.sub_yuanbo(Static.SIEGE_DELETE_CD_TIME_COST,info=u"攻城战清除CD")
    response.common_response.player.set("siegeBattle", player.SiegeBattle.to_dict())

    return response

@handle_common
@require_player
def siegeBattleFortReset(request, response):
    """
    攻城战堡垒信息重置
    """

    player = request.player
    fortIndexes = getattr(request.logic_request, "indexes", 0)

    # 检查等级
    if not player.isOpenSiege:
        AlertHandler(player, response, AlertID.ALERT_PLAYER_LEVEL_NOT_ENOUGH, u"siegeBattleFortReset:need level(%s) player level is %s" %(Static.SIEGE_LEVEL, player.level))
        return response

    diamondCost = 0
    now = time.time()
    fortInfos = player.SiegeBattle.fortInfos
    for fortIndex in fortIndexes:
        if not player.SiegeBattle.fort_canReset(fortIndex):
            continue

        fortCdAt = fortInfos[fortIndex - 1]
    
        _diamondCost = int(math.ceil((now - fortCdAt) * 1.0 / 60))
        _diamondCost = _diamondCost if _diamondCost > 0 else 0
        diamondCost += _diamondCost

    if player.yuanbo < diamondCost:
        AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"siegeBattleFortReset cost(%s) now player have (%s)" % (diamondCost, player.yuanbo))
        return response

    player.sub_yuanbo(diamondCost, info=u"攻城战堡垒信息重置")

    player.SiegeBattle.forts_reset(fortIndexes)
    response.common_response.player.set("siegeBattle", player.SiegeBattle.to_dict())

    return response


@handle_common
@require_player
def rampartSoldierLevelUp(request, response):
    player = request.player
    soldier_id = getattr(request.logic_request, "playerRampartSoldierId", 0)

    playerrampartsoldier = player.rampartSoldiers.get(int(soldier_id))
    if not playerrampartsoldier:
        raise ErrorException(player, u"rampartSoldierLevelUp:rampartSoldiers(%s) is not existed" % soldier_id)
    if not playerrampartsoldier.canLevelUp:
        return response

    playerrampartsoldier.levelUp()
    player.update_rampartsoldier(playerrampartsoldier, True)
    return response
