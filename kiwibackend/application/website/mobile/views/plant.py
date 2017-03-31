# -*- encoding:utf8 -*-
from decorators import require_player, handle_common
from module.common.static import Static, AlertID
from module.playerplant.api import  acquire_buildingplant
from module.building.api import get_building, get_building_count_by_level, get_buildingplant_by_buildingid
from module.common.middleware import ErrorException, AlertHandler
from module.common.actionlog import ActionLogWriter
from module.rewards.api import reward_cost_check, reward_cost, reward_send
from module.item.api import get_item
from module.vip.api import get_vip

@handle_common
@require_player
def buildingPlantBuild(request, response):
    """
    创建植物
    """
    centerX = getattr(request.logic_request, "centerX", 0)
    centerY = getattr(request.logic_request, "centerY", 0)
    building_id = getattr(request.logic_request, "buildingId", -1) # building 表主键
    player = request.player

    buildingplant = get_buildingplant_by_buildingid(building_id)
    if not buildingplant:
        raise ErrorException(player, u"buildingBuild:plant(%s) is not existed" % building_id)

    building = get_building(building_id)
    #检查单个植物总数
    building_count = get_building_count_by_level(building, player.castleLevel)
    if building_count <= 0:
        raise ErrorException(player, u"buildingBuild:plant(%s) create allow number is %s" % (building_id, building_count))
        return response
    playerbuilding_count = player.get_plants_count(buildingplant.pk)
    if playerbuilding_count >= building_count:
        AlertHandler(player, response, AlertID.ALERT_BUILDING_BUILD_OVER_MAX_NUMBER, u"buildingBuild:building(%s) create allow number is %s , already building number is %s" % (building_id, building_count, playerbuilding_count))
        return response
    #检查植物总数
    vip = get_vip(player.vip_level)
    if len(player.buildingplants.all()) >= vip.plantCount:
        AlertHandler(player, response, AlertID.ALERT_BUILDING_BUILD_OVER_MAX_NUMBER, u"buildingBuild:building(%s) create allow number is %s , already building number is %s" % (building_id, vip.plantCount, len(player.buildingplants.all())))
        return response
    #创建消耗检查
    costs = buildingplant.costs
    for cost in costs:  
        playeritem = player.items.get(cost.type)
        if not playeritem:
            raise ErrorException(player, u"itemUse:playeritem(%s) no existed" % (playeritem.pk))
        if not playeritem.can_sub(cost.count):
            #更新数据
            player.update_item(playeritem)
            AlertHandler(player, response, AlertID.ALERT_ITEM_NOT_ENOUGH,  u"itemUse:item(%s) playeritem(%s) useCount(%s) count(%s)" % (playeritem.item_id,cost.type, cost.count, playeritem.count))
            return response
        playeritem.sub(cost.count, u"物品使用")
    info = u"创建植物"
    playerbuildingplant = acquire_buildingplant(player, buildingplant, centerX = centerX, centerY = centerY, status = 0, buildingId = building_id)
    ActionLogWriter.building_create(player, playerbuildingplant.pk, playerbuildingplant.plantId, info)

    return response

@handle_common
@require_player
def buildingPlantPeriod(request, response):
    '''
    植物时期变化
    '''
    player = request.player
    playerplant_id = getattr(request.logic_request, "playerPlantId", -1)
    playerbuildingplant = player.buildingplants.get(playerplant_id)
    if not playerbuildingplant.can_change_status:
        #植物当前是成熟或枯萎状态，不用变化
        return response
    playerbuildingplant.check_status()
    player.update_buildingplant(playerbuildingplant, True)
    return response

@handle_common
@require_player
def buildingPlantHarvest(request, response):
    '''
    植物采摘
    '''
    player = request.player
    playerplant_id = getattr(request.logic_request, "playerPlantId", 0)
    playerbuildingplant = player.buildingplants.get(playerplant_id)
    if playerbuildingplant.harvestLeftTimes <= 0:
        AlertHandler(player, response, AlertID.ALERT_PLANT_HARVEST_OVER_MAX_NUMBER, u"buildingPlantHarvest:plant(%s) is not mature" % playerbuildingplant.plantId)
        return response
    if not playerbuildingplant.is_maturation:
        AlertHandler(player, response, AlertID.ALERT_PLANT_HARVEST_NOT_MATURATION, u"buildingPlantHarvest:plant(%s) is not mature" % playerbuildingplant.plantId)
        return response

    info = u"植物采摘奖励"
    rewards = []
    rewards = playerbuildingplant.harvest()
    for reward in rewards:
        reward_send(player, reward, info=info)
    player.update_buildingplant(playerbuildingplant, True)
    response.logic_response.set("rewards", [reward.to_dict() for reward in rewards])
    return response

@handle_common
@require_player
def buildingPlantDismantle(request, response):
    """
    植物铲除
    """
    player = request.player
    playerplant_id = getattr(request.logic_request, "playerPlantId", 0)
    playerplant = player.buildingplants.get(playerplant_id)
    if not playerplant: 
        raise ErrorException(player, u"plantDismantle:no playerbuildingplant(%s)" % (playerplant_id))
    player.delete_buildingplant(playerplant_id, True)
    return response