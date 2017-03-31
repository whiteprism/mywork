# -*- encoding:utf-8 -*-
from decorators import require_player, handle_common
from module.common.static import Static, AlertID
from module.player.api import get_player, filter_robots_by_level, get_pvp_players, get_robot_resource
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
            if player.siege_be_challenging:
                # 正在被攻击 不能进行匹配
                AlertHandler(player, response, AlertID.ALERT_SIEGE_BATTLE_BE_CHALLENGING, u"siegeBattlePlayer:be challenging")
                return response
            if target_player_id != player.SiegeBattle.oppId:
                # 匹配的对手和挑战的对手不统一
                AlertHandler(player,response, AlertID.ALERT_SIEGE_BATTLE_MATCH_AGAIN, u"pvpSetUp:siege fight player(%s) is not match player(%s)" % (target_player_id, player.SiegeBattle.oppId))
                return response

            # 移动堡垒检查
            if not player.SiegeBattle.has_fort:
                AlertHandler(player, response, AlertID.ALERT_SIEGE_BATTLE_NO_FORT, u"siegeBattlePlayer:fort is not enougth")
                return response
            if target_player_id > 0:
                target_player.siege_be_challenged() # 设置被挑战的时间
            player.siege_be_safedTime(240) # 攻击者被保护4分钟
            # 消耗一个移动堡垒
            player.SiegeBattle.use_fort()
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
    # send_battle_record(player=player, isWin=isWin, playerScore=player.PVP.score, playerRank=player.PVP.rank, targetPlayerScore=target_player.PVP.score, targetPlayerRank=target_player.PVP.rank, addScore=score,playerPowerRank = player.powerRank, targetPlayerId=target_player.pk,targetPlayerPowerRank=target_player.powerRank, playerVip=int(player.vip_level), playerIcon=player.iconId, targetPlayerVip=int(target_player.vip_level), targetPlayerIcon=target_player.iconId)
    send_battle_record(player=player, targetPlayer=target_player, isWin=isWin, category=1, addScore=score, playerHeroes=player.layoutHeroSimple_dict(), targetHeroes=target_player.layoutHeroSimple_dict())

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
    player = request.player
    isWin = getattr(request.logic_request, "isWin", False)
    soldiers = getattr(request.logic_request, "soldiers", [])
    targetId = getattr(request.logic_request, "oppId", False)

    if not player.isOpenSiege:
        AlertHandler(player,response, AlertID.ALERT_LEVEL_SHORTAGE, u"_siegeBattleResult:playerLevel(%s) startLevel(%s)" % (player.level, Static.SIEGE_LEVEL))
        return response
    # 目标玩家
    if int(targetId) != int(player.SiegeBattle.oppId):
        # 检验目标
        raise ErrorException(player, u"siegeBattleResult: SiegeBattle target player is not correct:target player id(%s) is not existed" % targetId)
    # 记录本次对战结果
    player.SiegeBattle.fightEnd(isWin)
    target_player = get_player(targetId)
    print '目标ＩＤ', targetId
    resource = {}
    if isWin:
        # 掠夺的资源
        if targetId > 0:
            # 真人
            resource = target_player.SiegeBattle.get_resources_settlement()
            target_player.siege_be_ended() # 清空攻击时间
            # 隐藏分变化
            player.add_liveness(18)
            target_player.sub_liveness(15)
            # 防守失败者有3小时的受保护时间
            print '设置保护时间3小时'
            target_player.set_lock_time()
        else:
            # 机器人
            resource = get_robot_resource(targetId)
            player.add_liveness(12)
        player.SiegeBattle.add_resource(resource)

    else:
        # 隐藏分变化
        if targetId > 0:
            player.add_liveness(6)
            target_player.sub_liveness(5)
            target_player.siege_be_ended() # 清空攻击时间
        else:
            player.add_liveness(4)

    player.cancel_protect_time() 
    # 将资源转化成奖励
    rewards = player.SiegeBattle.from_resource_to_reward(resource)
    send_battle_record(player=player, targetPlayer=target_player, isWin=isWin, category=2, playerHeroes=player.layoutSiegeHeroSimple_dict(), targetHeroes=target_player.layoutSiegeHeroSimple_dict(), playerWallSoldiers = soldiers, targetWallSoldiers= target_player.siege_wall_soldiers(), resource=resource)

    if target_player.id > 0:
        send_battle_record(player=target_player, targetPlayer=player, isWin=not isWin, category=2, playerHeroes=target_player.layoutSiegeHeroSimple_dict(), targetHeroes=player.layoutSiegeHeroSimple_dict(), playerWallSoldiers = target_player.siege_wall_soldiers(), targetWallSoldiers = soldiers, resource=resource)
    player.dailytask_going(Static.DAILYTASK_CATEGORY_SIEGE_BATTLE, number=1, is_incr=True, is_series=True)
    player.SiegeBattle.update()
    response.logic_response.set("rewards", [reward.to_dict() for reward in rewards])
    response.common_response.player.set("siegeBattle", player.SiegeBattle.to_dict())
    return response

@handle_common
@require_player
def siegeBattleResourceArrive(request, response):
    """
        攻城战资源到达
    """
    # 前端倒计时结束 向后端请求
    player = request.player
    index = getattr(request.logic_request, "index", 0)
    if index != 0:
        player.SiegeBattle.check_resource(index-1)
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
    category = getattr(request.logic_request, "category", 0) # 默认0正常匹配 1为确定取消保护再匹配

    if not player.isOpenSiege:
        AlertHandler(player, response, AlertID.ALERT_PLAYER_LEVEL_NOT_ENOUGH, u"siegeBattlePlayer:need level(%s) player level is %s" %(Static.SIEGE_LEVEL, player.level))
        return response
    if player.siege_be_challenging:
        # 正在被攻击 不能进行匹配
        AlertHandler(player, response, AlertID.ALERT_SIEGE_BATTLE_BE_CHALLENGING, u"siegeBattlePlayer:be challenging")
        return response

    # 运送车辆上限检查
    if not player.SiegeBattle.has_truck:
        AlertHandler(player, response, AlertID.ALERT_SIEGE_BATTLE_TRUCK_COUNT_IS_TOP, u"siegeBattlePlayer:truck count is top")
        return response
    if player.siege_in_safed:
        # 处于被保护阶段
        if category == 1:
            player.cancel_protect_time()
        else:
            response.logic_response.set("hasSafeTime", True)
            return response
    # 不释放上一个对手的话30秒自动过期
    opp = player.SiegeBattle.searchOpp()
    if opp.id > 0:
        resource = opp.SiegeBattle.get_resources() # 能被抢夺的资源
        opp.siege_be_searched() # 设置被搜到
    else:
        resource = get_robot_resource(opp.id)
    response.logic_response.set("resources", resource)
    response.logic_response.set("opp", opp.siege_view_data())
    response.common_response.player.set("siegeBattle", player.SiegeBattle.to_dict())
    return response

# TODO : 删掉
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

#TODO 删掉
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

    diamondCost = player.SiegeBattle.reset_fort_cost
    for fortIndex in fortIndexes:
        if player.SiegeBattle.can_reset_fort(fortIndex-1):
            print "OK"
            if player.yuanbo < diamondCost:
                AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"siegeBattleFortReset cost(%s) now player have (%s)" % (diamondCost, player.yuanbo))
                return response
            player.sub_yuanbo(diamondCost, info=u"攻城战堡垒信息重置")
            player.SiegeBattle.reset_fort(fortIndex-1)
            continue
    response.common_response.player.set("siegeBattle", player.SiegeBattle.to_dict())
    return response

