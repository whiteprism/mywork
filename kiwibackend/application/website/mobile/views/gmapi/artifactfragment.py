# -*- coding: utf-8 -*-
from decorators import *
from api import *
from opensocial.http import HttpResponseJson
from module.common.static import ErrorCode
from django.conf import settings

@handle_verification
def query_player_artifact_fragment(request):
    '''
        查询用户圣物碎片
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

    fragments = player.artifactfragments.all().values()
    data = []
    for fragment in fragments:
        meta = fragment.to_dict()
        meta["name"] = fragment.artifactfragment and fragment.artifactfragment.name or ""
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

    # fragments = player.artifactfragments.all().values()
    # data = []
    # for fragment in fragments:
    #     meta = fragment.to_dict()
    #     meta["name"] = fragment.artifactfragment and fragment.artifactfragment.name or ""
    #     data.append(meta)
    # return HttpResponseJson(data)

