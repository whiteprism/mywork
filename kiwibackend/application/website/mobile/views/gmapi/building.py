# -*- coding: utf-8 -*-
from decorators import *
from api import *
from opensocial.http import HttpResponseJson
from module.common.static import ErrorCode
from django.conf import settings

@handle_verification
def query_player_building(request):
    '''
        查询用户建筑
    '''
    playerId = request.REQUEST.get("playerId", "").strip()
    serverId = request.REQUEST.get("serverId", str(settings.SERVERID)).strip()
    player = get_player_by_id_or_str(playerId, int(serverId))

    resdata = {}
    if not player:
        resdata["success"] = False
        resdata["message"] = u"该玩家不存在!"
        resdata["data"] = []
        return HttpResponseJson(resdata)

    buildings = player.buildings.all().values()
    data = []
    for building in buildings:
        meta = building.to_dict()
        meta["name"] = building.building and building.building.name or ""
        data.append(meta)
    resdata["success"] = True
    resdata["message"] = ""
    resdata["data"] = data
    return HttpResponseJson(resdata)
    # if not player:
    #     data = {"success": False,
    #         "message": "The user does not exist!",
    #         "errorcode": ErrorCode.ERROR_PLAYER_IS_NONE
    #     }
    #     return HttpResponseJson(data)

    # buildings = player.buildings.all().values()
    # data = []
    # for building in buildings:
    #     meta = building.to_dict()
    #     meta["name"] = building.building and building.building.name or ""
    #     data.append(meta)
    # return HttpResponseJson(data)

@handle_verification
def query_player_buildingfragment(request):
    '''
        查询用户建筑碎片
    '''
    playerId = request.REQUEST.get("playerId", "").strip()
    serverId = request.REQUEST.get("serverId", str(settings.SERVERID)).strip()
    player = get_player_by_id_or_str(playerId, int(serverId))

    resdata = {}
    if not player:
        resdata["success"] = False
        resdata["message"] = u"该玩家不存在!"
        resdata["data"] = []
        return HttpResponseJson(resdata)

    fragments = player.buildingfragments.all().values()
    data = []
    for fragment in fragments:
        meta = fragment.to_dict()
        meta["name"] = fragment.buildingfragment and fragment.buildingfragment.name or ""
        data.append(meta)
    resdata["success"] = True
    resdata["message"] = ""
    resdata["data"] = data
    return HttpResponseJson(resdata)
    # if not player:
    #     data = {"success": False,
    #         "message": "The user does not exist!",
    #         "errorcode": ErrorCode.ERROR_PLAYER_IS_NONE
    #     }
    #     return HttpResponseJson(data)

    # fragments = player.buildingfragments.all().values()
    # data = []
    # for fragment in fragments:
    #     meta = fragment.to_dict()
    #     meta["name"] = fragment.buildingfragment and fragment.buildingfragment.name or ""
    #     data.append(meta)
    # return HttpResponseJson(data)

@handle_verification
def query_player_plant(request):
    '''
        查询用户植物
    '''
    playerId = request.REQUEST.get("playerId", "").strip()
    serverId = request.REQUEST.get("serverId", str(settings.SERVERID)).strip()
    player = get_player_by_id_or_str(playerId, int(serverId))

    resdata = {}
    if not player:
        resdata["success"] = False
        resdata["message"] = u"该玩家不存在!"
        resdata["data"] = []
        return HttpResponseJson(resdata)

    plants = player.buildingplants.all().values()
    data = []
    for plant in plants:
        meta = plant.to_dict()
        meta["name"] = plant.building and plant.building.name or ""
        data.append(meta)
    resdata["success"] = True
    resdata["message"] = ""
    resdata["data"] = data
    return HttpResponseJson(resdata)
    # if not player:
    #     data = {"success": False,
    #         "message": "The user does not exist!",
    #         "errorcode": ErrorCode.ERROR_PLAYER_IS_NONE
    #     }
    #     return HttpResponseJson(data)

    # plants = player.buildingplants.all().values()
    # data = []
    # for plant in plants:
    #     meta = plant.to_dict()
    #     meta["name"] = plant.building and plant.building.name or ""
    #     data.append(meta)
    # return HttpResponseJson(data)
