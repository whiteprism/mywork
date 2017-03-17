# -*- coding: utf-8 -*
from django.contrib.admin.views.decorators import  staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from gameconfig.api import get_models, get_model,check_func
import urllib, urllib2
import simplejson
from django.conf import settings
from common import *

@staff_member_required
def search_action(request):
    serverID = request.POST.get("server_id")
    userID = request.POST.get("player_id")
    print request.POST,"***********"
    data = request.POST.copy()
    data_urlencode = urllib.urlencode(data)
    url = "%s/check_player_action?" % settings.GM_URL
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
    "playerinfos":res["data"]
    }

    ctxt = RequestContext(request,resdata)

    return render_to_response("action/search_action.html", ctxt)
