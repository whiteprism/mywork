# -*- encoding:utf8 -*-
from decorators import require_player, handle_common
from module.common.static import Static, AlertID
from module.playerbuilding.api import  acquire_building
from module.building.api import get_building, get_building_count_by_level, get_building_upgrade_by_building_and_level, get_buildingproductions_by_building, get_buildingfragment
from module.hero.api import get_card
from module.building.api import BuildingGolden
import math
from module.rewards.api import reward_cost_check, reward_cost, reward_send
from module.common.middleware import ErrorException, AlertHandler
from module.common.actionlog import ActionLogWriter
from module.vip.api import get_vip
import random

@handle_common
@require_player
def buildingMove(request, response):
    """
    建筑物移动
    """
    playerbuilding_ids = getattr(request.logic_request, "buildings", 0)

    player = request.player

    for _pb in playerbuilding_ids:
        if not _pb["category"]:
            playerbuilding = player.buildings.get(_pb["key"])
            if not playerbuilding:
                raise ErrorException(player, u"buildingBuild:playerbuilding(%s) is not existed" % _pb["key"])
            playerbuilding.centerX = _pb["centerX"]
            playerbuilding.centerY = _pb["centerY"]
            player.update_building(playerbuilding, True)
        else:
            #植物
            playerplant = player.buildingplants.get(_pb["key"])
            if not playerplant:
                raise ErrorException(player, u"buildingBuild:playerplant(%s) is not existed" % _pb["key"])
            playerplant.centerX = _pb["centerX"]
            playerplant.centerY = _pb["centerY"]
            player.update_buildingplant(playerplant, True)

    return response

@handle_common
@require_player
def buildingBuild(request, response):
    '''
    创建建筑
    '''
    centerX = getattr(request.logic_request, "centerX", 0)
    centerY = getattr(request.logic_request, "centerY", 0)
    building_id = getattr(request.logic_request, "buildingId", -1)

    player = request.player

    building = get_building(building_id)
    if not building:
        raise ErrorException(player, u"buildingBuild:building(%s) is not existed" % building_id)

    building_upgrade = get_building_upgrade_by_building_and_level(building, 0)
    #能否升级等级检查
    if not building_upgrade:
        raise ErrorException(player, u"buildingBuild:building(%s) can not be created" % building_id)

    if building.is_castle:
        if building_upgrade.userLevel > player.level:
            AlertHandler(player, response, AlertID.ALERT_PLAYER_LEVEL_NOT_ENOUGH, u"buildingBuild:building(%s) upgrade  needlevel(%s) playerlevel(%s)" % (building_id, building_upgrade.userLevel, player.level))
            return response

    elif building_upgrade.castleLevel > player.castleLevel:
        AlertHandler(player, response, AlertID.ALERT_BUILDING_CASTLE_LEVEL_NOT_ENOUGH, u"buildingBuild:building(%s) upgrade  needlevel(%s) playercastlelevel(%s)" % (building_id, building_upgrade.castleLevel, player.castleLevel))
        return response

    #建造数量检查
    building_count = get_building_count_by_level(building, player.castleLevel)
    if building_count <= 0:
        AlertHandler(player, response, AlertID.ALERT_PLAYER_LEVEL_NOT_ENOUGH, u"buildingBuild:building(%s) create allow number is %s" % (building_id, building_count))
        return response
    #建造数量上限检查
    playerbuilding_count = player.get_buildings_count(building.pk)
    if playerbuilding_count >= building_count:
        AlertHandler(player, response, AlertID.ALERT_BUILDING_BUILD_OVER_MAX_NUMBER, u"buildingBuild:building(%s) create allow number is %s , already building number is %s" % (building_id, building_count, playerbuilding_count))
        return response

    #能否升级消耗检查
    for cost in building_upgrade.costs:
        if not reward_cost_check(player, cost):
            if building.is_statue:
                AlertHandler(player, response, AlertID.ALERT_BUILDING_MATERIAL_NOT_ENOUGH, u"buildingBuild:building(%s) create cost(%s) is error" % (building_id, cost.pk))
                return response
            AlertHandler(player, response, AlertID.ALERT_BUILDING_MATERIAL_NOT_ENOUGH, u"buildingBuild:building(%s) create cost(%s) is error" % (building_id, cost.pk))
            return response

    #建造神像数量检查
    if building.is_statue:
        #神像总数的检查
        vip = get_vip(player.vip_level)
        if player.get_statue_count(building_id) >= vip.statueCount:
            AlertHandler(player, response, AlertID.ALERT_BUILDING_BUILD_OVER_MAX_NUMBER, u"buildingBuild:building(%s) create allow number is %s , already building number is %s" % (building_id, Static.STATUE_MAX_COUNT, player.get_statue_count()))
            return response

    info = u"建造:%s" % building.name
    for cost in building_upgrade.costs:
        reward_cost(player, cost, info)

    playerbuilding = acquire_building(player, building, centerX = centerX, centerY = centerY, status = 0, info=info)
    #神像刚建造时
    building_upgrade = get_building_upgrade_by_building_and_level(playerbuilding.building, playerbuilding.level)

    # 建造铁匠铺
    if building.is_blacksmith:
        if player.tutorial_id == Static.TUTORIAL_ID_BLACK_SMITH_5:
            player.tutorial_complete()
            player.next_tutorial_open()
    #  建造金矿
    if building.is_goldmine:
        if player.tutorial_id == Static.TUTORIAL_ID_GOLDEN_7:
            player.tutorial_complete()
            player.next_tutorial_open()
    # 建造伐木场
    if building.is_loggingfield:
        if player.tutorial_id == Static.TUTORIAL_ID_LOGFIELD_8:
            player.tutorial_complete()

    if building.is_tarven:
        if player.tutorial_id == Static.TUTORIAL_ID_TAVERN_9:
            player.tutorial_complete()
            player.next_tutorial_open()

    if building.is_arena:
        if player.tutorial_id == Static.TUTORIAL_ID_ARENA_BUILD_17:
            player.tutorial_complete()
        player.setArenaOpen() #玩家可以被其他人搜索到
        player.PVP.reset_daily_data()
        player.arenashop.refresh_auto()
        response.common_response.player.set("honorShop", player.arenashop.to_dict())
        response.common_response.player.set("arena", player.PVP.to_dict())

    if building.is_elementtower:
        player.elementTower.init()
        response.common_response.player.set("elementTower", player.elementTower.to_dict())
        
    # 战争图腾建造　开启1700新手引导
    if building.is_hordelab:
        player.start_tutorial_by_id(Static.TUTORIAL_ID_INSTANCE_16)

    # 上古遗迹建造　开启1800新手引导
    if building.is_taitan:
        player.start_tutorial_by_id(Static.TUTORIAL_ID_INSTANCE_17)

    # 全视之眼建造　开启1900新手引导
    if building.is_radar:
        player.start_tutorial_by_id(Static.TUTORIAL_ID_INSTANCE_18)
        player.setSiegeOpen() #玩家可以被其他人搜到
        #城墙
        acquire_building(player, 1002002, level = 1 , centerX = 0, centerY = 0, status = 0, info=info)
        #城墙配置点
        point = player.castleLevel < 10 and range(1,4) or range(0, 5)
        defenseSiegeSoldierIds = player.castleLevel < 10 and [-1, 0, 0, 0, -1] or [0, 0, 0, 0, 0]
        for i in point:
            acquire_building(player, 1002003, level = 1 , centerX = i, centerY = 0, status = 0, info=info)
        #防御塔配置点
        for i in range(2):
            acquire_building(player, 1002004, level = 1 , centerX = i, centerY = 0, status = 0, info=info)
        player.update_siege_defenseSoldierIds(defenseSiegeSoldierIds)
        response.common_response.player.set("defenseSiegeSoldierIds", defenseSiegeSoldierIds)
        response.common_response.player.set("siegeBattle", player.SiegeBattle.to_dict())

    return response

@handle_common
@require_player
def buildingLevelUp(request, response):
    '''
    建筑升级
    '''
    player = request.player
    playerbuilding_id = getattr(request.logic_request, "playerBuildingId", 0)

    playerbuilding = player.buildings.get(playerbuilding_id)
    if not playerbuilding: 
        raise ErrorException(player, u"buildingLevelUp:no playerbuilding(%s)" % (playerbuilding_id))

    building_id = playerbuilding.building.pk
    if not playerbuilding.is_normal:
        if playerbuilding.is_upgrading:
            alert_id = AlertID.ALERT_BUILDING_IS_UPGRADING
        elif playerbuilding.is_producing:
            alert_id = AlertID.ALERT_BUILDING_IS_PRODUCING

        player.update_building(playerbuilding)
        AlertHandler(player, response, alert_id, u"buildingLevelUp:building(%s) upgrade playerbuilding(%s) status(%s) is not normal" % (building_id, playerbuilding_id, playerbuilding.status))
        return response

    building_upgrade = get_building_upgrade_by_building_and_level(playerbuilding.building, playerbuilding.level)
    #能否升级等级检查
    if not building_upgrade:
        raise ErrorException(player, u"buildingLevelUp:building(%s) upgrade playerbuilding(%s) level(%s) not upgrade info" % (building_id, playerbuilding_id, playerbuilding.level))
    
    if playerbuilding.building.is_castle:
        if building_upgrade.userLevel > player.level:
            AlertHandler(player, response, AlertID.ALERT_PLAYER_LEVEL_NOT_ENOUGH, u"buildingLevelUp:building(%s) upgrade playerbuilding(%s) needlevel(%s) playerlevel(%s)" % (building_id, playerbuilding_id, building_upgrade.userLevel, player.level))
            return response

    elif building_upgrade.castleLevel > player.castleLevel:
        AlertHandler(player, response, AlertID.ALERT_BUILDING_CASTLE_LEVEL_NOT_ENOUGH, u"buildingLevelUp:building(%s) upgrade playerbuilding(%s) needlevel(%s) playercastlelevel(%s)" % (building_id, playerbuilding_id, building_upgrade.castleLevel, player.castleLevel))
        return response


    #消耗检查
    for cost in building_upgrade.costs:
        if not reward_cost_check(player, cost):
            AlertHandler(player, response, AlertID.ALERT_BUILDING_MATERIAL_NOT_ENOUGH, u"buildingLevelUp:building(%s) upgrade cost(%s) is error" % (building_id, cost.pk))
            return response

    info = u"升级：%s->%s" % (playerbuilding.building.name , playerbuilding.level)
    for cost in building_upgrade.costs:
        reward_cost(player, cost, info)

    before_level = playerbuilding.level
    playerbuilding.upgrade(building_upgrade)
    if playerbuilding.building.is_statue and playerbuilding.level == 1:
        playerbuilding.random_attrbutes()

    after_level = playerbuilding.level
    ActionLogWriter.building_upgrade(player, playerbuilding.pk, playerbuilding.building_id, before_level, after_level, info)

    player.update_building(playerbuilding, True)
    return response

@handle_common
@require_player
def buildingCheck(request, response):
    '''
    建筑物升级结束
    '''
    player = request.player
    playerbuilding_id = getattr(request.logic_request, "playerBuildingId", 0)

    playerbuilding = player.buildings.get(playerbuilding_id)

    if not playerbuilding: 
        raise ErrorException(player, u"buildingCheck:no playerbuilding(%s)" % (playerbuilding_id))

    building_id = playerbuilding.building.pk
    if not playerbuilding.is_upgrading:
        player.update_building(playerbuilding)
        AlertHandler(player, response, AlertID.ALERT_BUILDING_IS_NOT_UPGRADING,u"buildingCheck:building(%s) harvest playerbuilding(%s) status(%s) is not normal" % (building_id, playerbuilding_id, playerbuilding.status))
        return response

    if playerbuilding.upgrade_over():
        player.update_building(playerbuilding, True)
    else:
        raise ErrorException(player, u"buildingCheck:building(%s) harvest playerbuilding(%s) is not over" % (building_id, playerbuilding_id))

    if playerbuilding.building.is_hordebarrack:
        player.update_hero_warriorIds(playerbuilding.building, playerbuilding.level)
        response.common_response.player.set("playerWarriorIds", player.playerWarriorIds)

    if playerbuilding.building.is_castle:
        player.update_castlelevel(playerbuilding.level)
        # 当要塞升到三级，开启1600
        if player.castleLevel == 2 and player.tutorial_id == Static.TUTORIAL_ID_CASTLE_LEVELUP_16:
            player.next_tutorial_open()
        elif player.castleLevel == 3:
            player.start_tutorial_by_id(Static.TUTORIAL_ID_CASTLE_LEVELUP3_18)
        elif player.castleLevel == 10 and player.isOpenSiege:
            #开锁最后两个配置点
            defenseSiegeSoldierIds = player.defenseSiegeSoldierIds
            for i in range(0, 5, 4):
                defenseSiegeSoldierIds[i] = 0
                acquire_building(player, 1002003, level = 1 , centerX = i, centerY = 0, status = 0)
            player.update_siege_defenseSoldierIds(defenseSiegeSoldierIds)
            response.common_response.player.set("defenseSiegeSoldierIds", player.defenseSiegeSoldierIds)

        player.task_going(Static.TASK_CATEGORY_CASTLE_LEVELUP, number=playerbuilding.level, is_incr=False, is_series=True)
    return response

@handle_common
@require_player
def buildingProduce(request, response):
    """
    生产兵 升级兵
    """
    player = request.player
    datas = getattr(request.logic_request, "buildings", [])

    # population = player.population
    # used_population = player.populationCost
    # _d["key"]玩家身上的建筑ｉｄ，并非建筑物ｉｄ

    for _d in datas:
        playerbuilding = player.buildings.get(_d["key"])
        if not playerbuilding: 
            raise ErrorException(player, u"buildingProduce:no playerbuilding(%s)" % (_d["key"]))

        building_id = playerbuilding.building.pk

        # 如果不是正常状态提示玩家，建筑正在工作.
        if not playerbuilding.is_normal:
            if playerbuilding.is_upgrading:
                alert_id = AlertID.ALERT_BUILDING_IS_UPGRADING
            elif playerbuilding.is_producing:
                alert_id = AlertID.ALERT_BUILDING_IS_PRODUCING

            player.update_building(playerbuilding)
            AlertHandler(player, response, alert_id, u"buildingProduce:building(%s) produce playerbuilding(%s) status(%s) is not normal" % (building_id, playerbuilding.id, playerbuilding.status))
            return response

    _production_level = 100

    for _d in datas:
        playerbuilding = player.buildings.get(_d["key"])
        playerbuilding.produce_soldier_begin()
        sort = 1

        # 通过建筑ｉｄ获取建筑产出物
        _productions = get_buildingproductions_by_building(playerbuilding.building)

        for _p in _d["productions"]:
            _production = None
            warrior = get_card(_p["production"]).warrior
            for _pp in _productions:

                for warrinfo in player.playerWarriorIds:
                    if warrinfo['soldierId'] == _p["production"]:
                        _production_level = warrinfo['soldierLevel']

                if _pp.buildingLevel <= playerbuilding.level and _pp.productionId == _p["production"] and _pp.productionLevel == _production_level:
                    _production = _pp
                    break
            if not _production:
                AlertHandler(player, response, Static.ALERT_BUILDING_HORDELAB_LEVEL_NOT_ENOUGH,)
                return response

            playerbuilding.produce_soldier(_p["production"], _p["productionCount"], _production, sort)

            if _production.is_drill:
                info = u"训练：%s" % warrior.name 
            else:
                info = u"升级：%s->%s" % (warrior.name, player.armies.level(_p["production"]))

            for cost in _production.cost:
                reward_cost(player, cost, info, number=_p["productionCount"])
            sort += 1
        playerbuilding.produce_soldier_end()

        player.update_building(playerbuilding, True)

    response.common_response.player.set("populationCost", player.populationCost)
    response.common_response.player.set("playerWarriorIds", player.playerWarriorIds)
    return response
    
@handle_common
@require_player
def buildingHarvest(request, response):
    '''
    采集
    '''
    player = request.player
    playerbuilding_id = getattr(request.logic_request, "playerBuildingId", 0)
    playerbuilding = player.buildings.get(playerbuilding_id)

    diamond_harvest = 0
    cal_proper = 33

    if not playerbuilding:
        raise ErrorException(player, u"buildingHarvest:no playerbuilding(%s)" % (playerbuilding_id))

    if playerbuilding.building.is_goldmine:
        # 金币收集有一定概率收集到　钻石。
        count = playerbuilding.goldmine_compute()
        # 收取金币随机收取一定量的钻石。具体方法超过最小采集上限，有百分之３０的概率获得金币
        gold_mine = BuildingGolden.get_buildinggolden_by_building(playerbuilding.building)
        gold_mine = gold_mine[playerbuilding.level - 1]

        if count > gold_mine.minHarvestScale and random.randint(1, 100) <= cal_proper:

            # 金币的收集数量和建筑物的等级有关系
            diamond_harvest = random.choice(range(playerbuilding.level, playerbuilding.level + 5))
            player.add_yuanbo(diamond_harvest, info=u"收取金币随机奖励")

        playerbuilding.goldmine_harvest()
        player.add_gold(count, info=u"金矿采集")
        player.task_going(Static.TASK_CATEGORY_GOLDENMINE_HARVEST, number=count, is_incr=True, is_series=True)
    elif playerbuilding.building.is_loggingfield:
        count = playerbuilding.goldmine_compute()
        playerbuilding.goldmine_harvest()
        player.add_wood(count, info=u"木材采集")
        player.task_going(Static.TASK_CATEGORY_WOOD_HARVEST, number=count, is_incr=True, is_series=True)

    elif playerbuilding.is_producing:
        playerbuilding.producing_soldier(player)
        response.common_response.player.set("soldiers", player.armies.to_dict())
        response.common_response.player.set("populationCost", player.populationCost)
        response.common_response.player.set("playerWarriorIds", player.playerWarriorIds)
    else:
        player.update_building(playerbuilding)
        AlertHandler(player, response, AlertID.ALERT_BUILDING_HARVEST_CAN_NOT, u"buildingHarvest:building(%s) playerbuilding(%s) can not harvest" % (playerbuilding.building_id, playerbuilding_id))
        return response

    player.update_building(playerbuilding, True)

    response.logic_response.set("diamondCount", diamond_harvest)
    response.logic_response.set("playerBuildingId", playerbuilding_id)
    return response

@handle_common
@require_player
def buildingSpeed(request, response):
    """
    加速
    """
    player = request.player
    playerbuilding_id = getattr(request.logic_request, "playerBuildingId", 0)
    playerbuilding = player.buildings.get(playerbuilding_id)

    if not playerbuilding: 
        raise ErrorException(player, u"buildingSpeed:no playerbuilding(%s)" % (playerbuilding_id))

    building_id = playerbuilding.building.pk
    if playerbuilding.is_normal:
        player.update_building(playerbuilding)
        AlertHandler(player, response, AlertID.ALERT_BUILDING_SPEED_CAN_NOT, u"buildingSpeed:building(%s)  playerbuilding(%s) status(%s) is  normal" % (building_id, playerbuilding_id, playerbuilding.status))
        return response
    #加速元宝数量检查
    left_time = playerbuilding.timeLeft
    delta_minute = int(math.ceil(left_time / 60.0))

    yuanbo = 0.0 #加速消耗元宝
    if delta_minute <= 60:
        yuanbo = delta_minute * 2
    elif delta_minute <= 600:
        yuanbo = delta_minute * 1.7 + 18
    else:
        yuanbo = delta_minute * 1.2 + 318

    yuanbo = int(math.ceil(yuanbo))


    if yuanbo > player.yuanbo:
        AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"buildingSpeed:building(%s)  playerbuilding(%s) costYuanbo(%s) playerYuanbo(%s)" % (building_id, playerbuilding_id, yuanbo,player.yuanbo ))
        return response

    if playerbuilding.is_upgrading:
        if playerbuilding.upgrade_over(speed=True):
            if playerbuilding.building.is_castle:
                player.update_castlelevel(playerbuilding.level)
                if player.castleLevel == 3:
                    player.start_tutorial_by_id(Static.TUTORIAL_ID_CASTLE_LEVELUP3_18)
                elif player.castleLevel == 10 and player.isOpenSiege:
                    #开锁最后两个配置点
                    defenseSiegeSoldierIds = player.defenseSiegeSoldierIds
                    for i in range(0, 5, 4):
                        defenseSiegeSoldierIds[i] = 0
                        acquire_building(player, 1002003, level = 1 , centerX = i, centerY = 0, status = 0)
                    player.update_siege_defenseSoldierIds(defenseSiegeSoldierIds)
                    response.common_response.player.set("defenseSiegeSoldierIds", player.defenseSiegeSoldierIds)
            if playerbuilding.building.is_hordebarrack:
                player.update_hero_warriorIds(playerbuilding.building, playerbuilding.level)
                if player.tutorial_id == Static.TUTORIAL_ID_CASTLE_LEVELUP3_18:
                    player.tutorial_complete()
                response.common_response.player.set("playerWarriorIds", player.playerWarriorIds)

            player.task_going(Static.TASK_CATEGORY_CASTLE_LEVELUP, number=playerbuilding.level, is_incr=False, is_series=True)
            player.update_building(playerbuilding, True)
            player.sub_yuanbo(yuanbo, info=u"加速升级:%s" % playerbuilding.building.name)

    elif playerbuilding.is_producing:
        if playerbuilding.producing_soldier(player, speed=True):
            player.update_building(playerbuilding, True)
            player.sub_yuanbo(yuanbo, info=u"加速生产:%s" % playerbuilding.building.name)
            response.common_response.player.set("playerWarriorIds", player.playerWarriorIds)
            response.common_response.player.set("populationCost", player.populationCost)

    return response


@handle_common
@require_player
def buildingTutorialEnd(request, response):

    """
    加速
    """
    player = request.player
    player.tutorial_complete()

    response.common_response.player.set("tutorial", player.tutorial)

    return response

@handle_common
@require_player
def buildingDismantle(request, response):
    """
    建筑拆除
    """
    player = request.player
    playerbuilding_id = getattr(request.logic_request, "playerBuildingId", 0)
    rewards = []
    playerbuilding = player.buildings.get(playerbuilding_id)
    if not playerbuilding: 
        raise ErrorException(player, u"buildingDismantle:no playerbuilding(%s)" % (playerbuilding_id))

    if not playerbuilding.building.canRemove:
        raise ErrorException(player, u"buildingDismantle:can not dismantle(%s)" % (playerbuilding_id))

    info = u"建筑拆除"
    rewards = playerbuilding.building.removeRewardIds
    for reward in rewards:
        reward_send(player, reward, info=info)
    player.delete_building(playerbuilding_id, True)
    ActionLogWriter.building_delete(player, playerbuilding_id, playerbuilding.building_id, info)
    response.logic_response.set("rewards", [reward.to_dict() for reward in rewards])
    return response

@handle_common
@require_player
def buildingWallWarriorUpgrade(request, response):
    """
    科技树升级
    """
    player = request.player
    warriorId = getattr(request.logic_request, "warriorId", 0) # 要升级的warriorIDs
    player.levelup_wall_warriors(warriorId)
    response.common_response.player.set("wallWarriorIds", player.wallWarriorIds)
    return response
