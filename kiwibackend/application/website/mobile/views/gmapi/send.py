# -*- coding: utf-8 -*-
from decorators import *
from api import *
from opensocial.http import HttpResponseJson
from module.common.static import ErrorCode
from django.conf import settings
from module.rewards.api import *

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
