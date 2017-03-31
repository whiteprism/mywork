# -*- coding: utf-8 -*-
from decorators import *
from api import *
from opensocial.http import HttpResponseJson
from module.common.static import ErrorCode
from module.mail.api import send_system_mail, get_mails
from django.conf import settings

@handle_verification
def send_mail(request):
    '''
        发送邮件
    '''
    playerIdList_int = request.REQUEST.get("playerIdList", "").strip() # 逗号隔开的id字符串
    serverId = request.REQUEST.get("serverId", str(settings.SERVERID)).strip()
    title = request.REQUEST.get("title", "").strip() # "fytext_300723"
    attachments_str = request.REQUEST.get("attachments", "").strip() # t1000c1002,t1001c1003
    content = request.REQUEST.get("content", "").strip() # "fytext_301064"
    paramList = request.REQUEST.get("paramList", "").strip()

    print title,"*****"
    if playerIdList_int == "all":
        players = get_all_player()
    else:
        players = [pk for pk in playerIdList_int.strip().split(",") if pk]

    rewards = []
    attachments = [pk for pk in attachments_str.strip().split(",") if pk]
    for attachment in attachments:
        reward = get_commonreward(attachment)
        rewards.append({
                "type": reward.type,
                "count": reward.count
            })

    contents = []
    paramList = [pk for pk in paramList.strip().split(",") if pk]
    contents.append({
        "content" : content,
        "paramList": paramList
    })

    data = []
    for player in players:
        if not isinstance(player, Player):
            _player = get_player_by_id_or_str(player, int(serverId))
        else:
            _player = player
        meta = {}
        meta["success"] = False
        if not _player:
            meta["id"] = player
            meta["message"] = u"该玩家不存在!"
            meta["errorcode"] = ErrorCode.ERROR_PLAYER_IS_NONE
            data.append(meta)
            continue
        send_system_mail(player=_player, sender=None, title=title, contents=contents, rewards=rewards)
        meta["id"] = _player.id
        meta["success"] = True
        meta["message"] = "Send success!"
        data.append(meta)

    return HttpResponseJson(data)

@handle_verification
def query_player_mails(request):
    '''
        查询玩家邮件
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

    mails = get_mails(player)
    data = []
    for mail in mails:
        data.append(mail.to_dict())

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

    # mails = get_mails(player)
    # data = []
    # for mail in mails:
    #     data.append(mail.to_dict())

    # return HttpResponseJson(data)
