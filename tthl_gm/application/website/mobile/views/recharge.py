# -*- coding: utf-8 -*
from django.contrib.admin.views.decorators import  staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext
import urllib, urllib2
import simplejson
from django.conf import settings
from common import *

@staff_member_required
def search_recharge(request):
    data = request.POST.copy()
    data_urlencode = urllib.urlencode(data)
    url = "%s/check_recharge_info?" % settings.GM_URL
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
        resdata = {
        "ret":res["ret"],
        "msg":res["msg"],
        "playerinfos":res["data"]
        }

        ctxt = RequestContext(request,resdata)

        return render_to_response("action/search_action.html", ctxt)
    else:
        return render_to_response("user/data_not_found.html")
