# -*- encoding:utf8 -*-
from decorators import require_player, handle_common
import random, time,datetime
from module.playeractivity.api import update_playeractivities
from module.playerinstance.api import get_player_view_instance_dict, get_player_open_raidinstance
from module.playerPVP.api import get_lastweek_rank, get_yesterday_rank
from module.common.static import Static

@handle_common
@require_player
def sync(request, response):

    player = request.player
    #跨天数据检查
    player.dailyCheck()
    now = datetime.datetime.now()

    response.common_response.player.set("raidInstance", {"instances":get_player_open_raidinstance(player)})
    if now.date() != player.updated_at.date():
        response.common_response.player.set("dailytasks", player.dailytask_dicts())
        response.common_response.player.set("instance", get_player_view_instance_dict(player))
        response.common_response.player.set("guild", player.guild.to_dict(True, True))
        response.common_response.player.set("elementTower", player.elementTower.to_dict())

        update_playeractivities(player)
        playeractivities = player.activities.all().values()
        activities = []
        for playeractivity in playeractivities:
            if playeractivity.activity.isOpen(player.userid):
                activities.append(playeractivity.to_dict())

        response.common_response.player.set("activities", activities)


                #player.update_activity(playeractivity)

    response.common_response.player.set("tavern", player.tavern)
    playerbuildings = player.buildings.all().values()
    for playerbuilding in playerbuildings:
        if playerbuilding.check_upgrade():
            player.update_building(playerbuilding)

    playerbuildingplants = player.buildingplants.all().values()
    for playerplant in playerbuildingplants:
        playerplant.check_status()
        player.update_buildingplant(playerplant)
    response.common_response.player.set("dailytasks", player.seven_days_task_dicts())

    response.common_response.player.set("dailyOppdata", get_yesterday_rank())
    response.common_response.player.set("weekOppdata", get_lastweek_rank())

    response.common_response.player.set("soldiers", player.armies.to_dict())
    # response.common_response.player.set("waravoidCDTime", player.waravoidCDTime)
    response.common_response.player.set("smallGameLeftTimes", player.smallGameLeftTimes)
        
    if player.mysteryshop.refresh_auto():
        response.common_response.player.set("mysteryShop", player.mysteryshop.to_dict())
    #PVP
    if player.isOpenArena:
        player.arenashop.refresh_auto()
        response.common_response.player.set("honorShop", player.arenashop.to_dict())
        response.common_response.player.set("arena", player.PVP.to_dict())
    #攻城战
    if player.isOpenSiege:
        # if player.SiegeBattle.refresh_auto():
            response.common_response.player.set("siegeBattle", player.SiegeBattle.to_dict())

    if player.guildshop.refresh_auto():
        response.common_response.player.set("guildshop", player.guildshop.to_dict(True))
    response.common_response.set("serverTime", int(time.time()))
    return response

@handle_common
@require_player
def wakeup(request, response):
    player = request.player
    player.dailyCheck()
    now = datetime.datetime.now()

    response.common_response.player.set("raidInstance", {"instances":get_player_open_raidinstance(player)})
    if now.date() != player.updated_at.date():
        response.common_response.player.set("dailytasks", player.dailytask_dicts())
        response.common_response.player.set("instance", get_player_view_instance_dict(player))
        response.common_response.player.set("guild", player.guild.to_dict(True, True))
        
        response.common_response.player.set("elementTower", player.elementTower.to_dict())

        update_playeractivities(player)
        playeractivities = player.activities.all().values()
        activities = []
        for playeractivity in playeractivities:
            if playeractivity.activity.isOpen(player.userid):
                activities.append(playeractivity.to_dict())

        response.common_response.player.set("activities", activities)

    update_playeractivities(player)
    response.common_response.player.set("tavern", player.tavern)
    playerbuildings = player.buildings.all().values()
    for playerbuilding in playerbuildings:
        playerbuilding.check_upgrade()
        player.update_building(playerbuilding)

    playerbuildingplants = player.buildingplants.all().values()
    for playerplant in playerbuildingplants:
        playerplant.check_status()
        player.update_buildingplant(playerplant)
        
    response.common_response.player.set("soldiers", player.armies.to_dict())
    # response.common_response.player.set("waravoidCDTime", player.waravoidCDTime)
    response.common_response.player.set("smallGameLeftTimes", player.smallGameLeftTimes)
        
    if player.mysteryshop.refresh_auto():
        response.common_response.player.set("mysteryShop", player.mysteryshop.to_dict())
    #PVP
    if player.isOpenArena:
        player.arenashop.refresh_auto()
        response.common_response.player.set("honorShop", player.arenashop.to_dict())
        response.common_response.player.set("arena", player.PVP.to_dict())
    #攻城战
    if player.isOpenSiege:
        # if player.SiegeBattle.refresh_auto():
        response.common_response.player.set("siegeBattle", player.SiegeBattle.to_dict())

    if player.guildshop.refresh_auto():
        response.common_response.player.set("guildshop", player.guildshop.to_dict(True))
    response.common_response.set("serverTime", int(time.time()))

    #飞鸽传书
    response.common_response.player.set("feiBook", player.guild.getFeiBookInfo())
    
    return response
