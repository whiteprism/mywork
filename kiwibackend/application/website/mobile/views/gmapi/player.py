# -*- coding: utf-8 -*-
from decorators import *
from api import *
from opensocial.http import HttpResponseJson
from module.common.static import ErrorCode
from django.conf import settings

@handle_verification
def query_player(request):
    '''
        查询用户
    '''
    playerIds = request.REQUEST.get("playerId", "").strip()
    serverId = request.REQUEST.get("serverId", str(settings.SERVERID)).strip()

    playerIds = [playerId for playerId in playerIds.strip().split(",") if playerId]
    print playerIds,"***"
    data = []
    for playerId in playerIds:
        player = get_player_by_id_or_str(playerId, int(serverId))
        if not player:
            meta = {"success": False,
                "message": u"该玩家不存在!",
                "player": {
                "id":playerId,
                }
            }
            data.append(meta)
            continue

        meta = {
            "player":{
                "id":player.id,
                "name": player.name,
                "level": player.level,
                "xp": player.xp,
                "gold": player.gold,
                "power": player.power,
                "stamina": player.stamina,
                "yuanbo": player.yuanbo,
                "wood": player.wood,
                "couragepoint": player.couragepoint,
                "gashaponInfos": {
                    "gold": {
                        "freeNumber": player.gashaponInfos["gold"]["freeNumber"],
                        "last": player.gashaponInfos["gold"]["last"].strftime("%Y-%m-%d %H:%M:%S")
                    },
                    "yuanbo": {
                         "last": player.gashaponInfos["yuanbo"]["last"].strftime("%Y-%m-%d %H:%M:%S")
                    }
                },
                "lastInstance": player.lastInstance,
                "lastEliteInstance": player.lastEliteInstance,
                "dailyTasks": player.dailyTasks,
                "tasks": player.tasks,
                "sevenDaystasks": player.sevenDaystasks,
                "completeSevenTasks": player.completeSevenTasks,
                "tutorial": player.tutorial,
                "deviceId": player.deviceId,
                "week_card": {
                    "status": player.week_card["status"],
                    "ended_at": player.week_card["ended_at"]
                },
                "month_card": {
                    "status": player.month_card["status"],
                    "ended_at": player.month_card["ended_at"]
                },
                "castleLevel": player.castleLevel,
                "playerWarriorIds": player.playerWarriorIds,
                "isOpenSiege": player.isOpenSiege,
                "isOpenArena": player.isOpenArena,
                "halfBuyIds": player.halfBuyIds,
                "powerRank": player.powerRank,
                "towerGold": player.towerGold,
                "activityValue": player.activityValue,
                "banAt": player.banAt.strftime("%Y-%m-%d %H:%M:%S"),
                "gagAt": player.gagAt.strftime("%Y-%m-%d %H:%M:%S"),
                "vip": player.vip,
                "createTime": player.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "lastLoginTime": player.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            },
            "success": True
        }
        if player.week_card["ended_at"]:
            meta["player"]["week_card"]["ended_at"] = player.week_card["ended_at"].strftime("%Y-%m-%d %H:%M:%S")
        if player.month_card["ended_at"]:
            meta["player"]["month_card"]["ended_at"] = player.month_card["ended_at"].strftime("%Y-%m-%d %H:%M:%S")
        data.append(meta)

    return HttpResponseJson(data)

@handle_verification
def ban_player(request):
    '''
        封号
    '''
    playerIdList_int = request.REQUEST.get("playerIdList", "").strip() # 逗号隔开的id字符串
    banAt = request.REQUEST.get("banAt", "").strip() # 时间字符串 格式：xxxx-xx-xx xx:xx:xx
    serverId = request.REQUEST.get("serverId", str(settings.SERVERID)).strip()

    data = []
    playerIds = [pk for pk in playerIdList_int.strip().split(",") if pk]
    for playerId in playerIds:
        player = get_player_by_id_or_str(playerId, int(serverId))
        meta = {}
        meta["success"] = False
        meta["id"] = playerId
        if not player:
            meta["message"] = u"该玩家不存在!"
            meta["errorcode"] = ErrorCode.ERROR_PLAYER_IS_NONE
            data.append(meta)
            continue
        if not player.setBanAt(banAt):
            meta["message"] = "封号失败!"
            meta["errorcode"] = ErrorCode.ERROR_SET_FAILED
            data.append(meta)
            continue
        meta["success"] = True
        meta["message"] = "封号成功!"
        data.append(meta)

    return HttpResponseJson(data)

@handle_verification
def gag_player(request):
    '''
        禁言
    '''
    playerIdList_int = request.REQUEST.get("playerIdList", "").strip() # 逗号隔开的id字符串
    gagAt = request.REQUEST.get("gagAt", "").strip() # 时间字符串 格式：xxxx-xx-xx xx:xx:xx
    serverId = request.REQUEST.get("serverId", str(settings.SERVERID)).strip()

    data = []
    playerIds = [pk for pk in playerIdList_int.strip().split(",") if pk]
    for playerId in playerIds:
        player = get_player_by_id_or_str(playerId, int(serverId))
        meta = {}
        meta["success"] = False
        meta["id"] = playerId
        if not player:
            meta["message"] = u"该玩家不存在!"
            meta["errorcode"] = ErrorCode.ERROR_PLAYER_IS_NONE
            data.append(meta)
            continue
        if not player.setGagAt(gagAt):
            meta["message"] = "禁言失败!"
            meta["errorcode"] = ErrorCode.ERROR_SET_FAILED
            data.append(meta)
            continue
        meta["success"] = True
        meta["message"] = "禁言成功!"
        data.append(meta)

    return HttpResponseJson(data)
