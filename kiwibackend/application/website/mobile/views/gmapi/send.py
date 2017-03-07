# -*- coding: utf-8 -*-
from decorators import *
from api import *
from opensocial.http import HttpResponseJson
from module.common.static import ErrorCode
from django.conf import settings
from module.rewards.api import *
from module.rewards.api import get_commonreward

@handle_verification
def send_item(request):
    playerId = request.REQUEST.get("playerId", "").strip()
    serverId = request.REQUEST.get("serverId", str(settings.SERVERID)).strip()
    itemType = request.REQUEST.get("itemType")
    count = request.REQUEST.get("itemCount")
    level = request.REQUEST.get("level",0)
    player = get_player_by_id_or_str(playerId, int(serverId))

    resdata = {}
    if not player:
        resdata["success"] = False
        resdata["message"] = u"该玩家不存在!"
        return HttpResponseJson(resdata)

    playeritem = player.items.get(int(itemType))
    print playeritem
    if not playeritem:
        #raise ErrorException(player, u"itemUse:playeritem(%s) no existed" % (playeritem_id))
        resdata["success"] = False
        resdata["message"] = u"物品不存在!"
        return HttpResponseJson(resdata)

    reward = CommonReward(int(itemType), int(count), int(level))
    reward_send(player,reward)
    player.save()
    resdata["success"] = True
    resdata["message"] = ""

    return HttpResponseJson(resdata)

@handle_verification
def delete_item(request):
    playerId = request.REQUEST.get("playerId", "").strip()
    serverId = request.REQUEST.get("serverId", str(settings.SERVERID)).strip()
    itemType = request.REQUEST.get("itemType")
    count = request.REQUEST.get("itemCount")
    level = request.REQUEST.get("level",0)
    player = get_player_by_id_or_str(playerId, int(serverId))

    resdata = {}
    if not player:
        resdata["success"] = False
        resdata["message"] = u"该玩家不存在!"
        return HttpResponseJson(resdata)

    playeritem = player.items.get(int(itemType))
    if not playeritem:
        #raise ErrorException(player, u"itemUse:playeritem(%s) no existed" % (playeritem_id))
        resdata["success"] = False
        resdata["message"] = u"物品不存在!"
        return HttpResponseJson(resdata)
    playeritem.sub(int(count),u"GM删除物品")
    player.save()
    resdata["success"] = True
    resdata["message"] = ""

    return HttpResponseJson(resdata)

@handle_verification
def send_items(request):
    playerId = request.REQUEST.get("playerId", "").strip()
    serverId = request.REQUEST.get("serverId", str(settings.SERVERID)).strip()
    items_str = request.REQUEST.get("items")
    player = get_player_by_id_or_str(playerId, int(serverId))

    resdata = {}
    resdata["data"] = []
    if not player:
        resdata["success"] = False
        resdata["message"] = u"该玩家不存在!"
        return HttpResponseJson(resdata)

    data = []
    items = [pk for pk in items_str.strip().split(",") if pk]
    for item in items:
        meta = {}
        itemType,count,level = get_item(item)
        meta["itemId"] = itemType
        playeritem = player.items.get(int(itemType))
        if not playeritem:
            #raise ErrorException(player, u"itemUse:playeritem(%s) no existed" % (playeritem_id))
            meta["success"] = False
            meta["message"] = u"物品不存在!"
        else:
            reward  = get_commonreward(item)
            reward_send(player,reward)
            meta["success"] = True
            meta["message"] = u"发放物品成功!"
        player.save()
        data.append(meta)
    resdata["success"] = True
    resdata["message"] = ""
    resdata["data"] = data

    return HttpResponseJson(resdata)

@handle_verification
def delete_items(request):
    playerId = request.REQUEST.get("playerId", "").strip()
    serverId = request.REQUEST.get("serverId", str(settings.SERVERID)).strip()
    items_str = request.REQUEST.get("items")
    player = get_player_by_id_or_str(playerId, int(serverId))

    resdata = {}
    if not player:
        resdata["success"] = False
        resdata["message"] = u"该玩家不存在!"
        resdata["data"] = []
        return HttpResponseJson(resdata)

    data = []
    items = [pk for pk in items_str.strip().split(",") if pk]
    for item in items:
        meta = {}
        itemType,count,level = get_item(item)
        meta["itemId"] = itemType
        playeritem = player.items.get(int(itemType))
        if not playeritem:
            #raise ErrorException(player, u"itemUse:playeritem(%s) no existed" % (playeritem_id))
            meta["success"] = False
            meta["message"] = u"物品不存在!"
        else:
            playeritem.sub(int(count),u"GM删除物品")
            meta["success"] = True
            meta["message"] = u"删除成功!"
        player.save()
        data.append(meta)
    resdata["success"] = True
    resdata["message"] = ""
    resdata["data"] = data
    return HttpResponseJson(resdata)
