# -*- coding: utf-8 -*
from django.contrib.admin.views.decorators import  staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from gameconfig.api import get_models, get_model,check_func
from servers.api import get_server_by_request
import urllib, urllib2
import simplejson
from django.conf import settings
from common import *

@staff_member_required
def search_action(request):
    userID = request.POST.get("player_id")
    print request.POST,"***********"
    data = request.POST.copy()
    server = get_server_by_request(request)
    data["server_id"] = server.id
    serverID = server.id
    data_urlencode = urllib.urlencode(data)
    url = "%s/check_player_action?" % server.gm_url
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
    if not res.has_key("data"):
        res["data"] = []
    resdata = {
    "ret":res["ret"],
    "msg":res["msg"],
    "playeractions":res["data"]
    }

    ctxt = RequestContext(request,resdata)

    return render_to_response("action/search_action.html", ctxt)
