# -*- coding: utf-8 -*
from django.contrib.admin.views.decorators import  staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from gameconfig.api import get_models, get_model,check_func
import urllib, urllib2
import simplejson
from module.server.api import get_server_by_request
from common import *

FUNC_USER_BAN = 3
FUNC_USER_GAG = 2

@staff_member_required
def search(request):
    '''
    查询玩家信息
    '''
    server = get_server_by_request(request)
    userID = request.POST.get("playerId")
    data = dict(request.POST.items())
    data["severId"] = server.id
    data["playerId"] = ','.join(data["playerId"].split("\r\n"))
    data_urlencode = urllib.urlencode(data)
    url = "%s/gmapi/player/query/?" % server.gm_url
    url_get = url + data_urlencode
    result,dt = url_request_handler(url_get)
    if result:
        response = dt
    else:
        msg_dict = dt
        ctxt = RequestContext(request,msg_dict)
        return render_to_response("error.html", ctxt)
    res = simplejson.loads(response.read())
    # if res.has_key("player"):
    canBan = check_func(request, FUNC_USER_BAN)
    canGag = check_func(request, FUNC_USER_GAG)

    resdata = {
        "serverID":server.pk,
        "userID":userID,
        "canBan":canBan,
        "canGag":canGag,
        "playerinfos":res
    }
    print resdata,"$$$$"
    ctxt = RequestContext(request,resdata)

    return render_to_response("user/search.html", ctxt)


@staff_member_required
def ban(request):
    '''
    封号
    '''
    #serverID = request.POST.get("serverID")
    userID = request.POST.get("userID")
    serverID = request.POST.get("serverID")
    # canBan = check_func(request, FUNC_USER_BAN)

    if not check_func(request, FUNC_USER_BAN):
        return render_to_response("error.html")



    data = {}
    data["canBan"] = check_func(request, FUNC_USER_BAN)
    data["canGag"] = check_func(request, FUNC_USER_GAG)
    data["serverID"] = serverID
    data["userID"] = userID

    data["users"] = [
        {
            "name" : u"张全明",
            "id":  1,
            "vip": 10,
            "level" : 11,
            "isBan": True,
            "isGag": True,

        },
        {
            "name" : u"张全明1",
            "id":  2,
            "vip": 10,
            "level" : 11,
            "isBan": True,
            "isGag": True,
        },
        {
            "name" : u"张全明2111",
            "id":  3,
            "vip": 10,
            "level" : 11,
            "isBan": True,
            "isGag": True,
        }
    ]

    ctxt = RequestContext(request,data)

    return render_to_response("user/search.html", ctxt)


@staff_member_required
def gag(request):
    '''
    禁言
    '''
    serverID = request.POST.get("serverID")
    userID = request.POST.get("userID")

    if not check_func(request, FUNC_USER_GAG):
        return render_to_response("error.html")


    data = {}
    data["canBan"] = check_func(request, FUNC_USER_BAN)
    data["canGag"] = check_func(request, FUNC_USER_GAG)
    data["serverID"] = serverID
    data["userID"] = userID

    data["users"] = [
        {
            "name" : u"张全明",
            "id":  1,
            "vip": 10,
            "level" : 11,
            "isBan": True,
            "isGag": True,

        },
        {
            "name" : u"张全明1",
            "id":  2,
            "vip": 10,
            "level" : 11,
            "isBan": True,
            "isGag": True,
        },
        {
            "name" : u"张全明2111",
            "id":  3,
            "vip": 10,
            "level" : 11,
            "isBan": True,
            "isGag": True,
        }
    ]

    ctxt = RequestContext(request,data)

    return render_to_response("user/search.html", ctxt)
