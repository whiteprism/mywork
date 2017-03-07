# -*- coding: utf-8 -*
from django.contrib.admin.views.decorators import  staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from gameconfig.api import get_models, get_model,check_func
import urllib, urllib2
import simplejson
from django.conf import settings

FUNC_USER_BAN = 3
FUNC_USER_GAG = 2

@staff_member_required
def search(request):
    serverID = request.POST.get("server_id")
    userID = request.POST.get("player_id")
    data = request.POST.copy()
    print data
    print ','.join(data["player_id"].split("\r\n"))
    data["player_id"] = ','.join(data["player_id"].split("\r\n"))
    data_urlencode = urllib.urlencode(data)
    url = "%s/check_player_info?" % settings.GM_URL
    url_get = url + data_urlencode
    result,dt = url_request_handler(url_get)
    if result:
        response = dt
    else:
        msg_dict = dt
        ctxt = RequestContext(request,msg_dict)
        return render_to_response("error.html", ctxt)
    a = response.read()
    print "response:",a, type(a)
    res = simplejson.loads(a)
    if res.has_key("data"):
        canBan = check_func(request, FUNC_USER_BAN)
        canGag = check_func(request, FUNC_USER_GAG)

        resdata = {
        "serverID":serverID,
        "userID":userID,
        "canBan":canBan,
        "canGag":canGag,
        "ret":res["ret"],
        "msg":res["msg"],
        "playerinfos":res["data"]
        }

        ctxt = RequestContext(request,resdata)

        return render_to_response("user/search.html", ctxt)
    else:
        return render_to_response("user/user_not_found.html")


@staff_member_required
def ban(request):
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