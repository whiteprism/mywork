# -*- coding: utf-8 -*
from django.contrib.admin.views.decorators import  staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext
import urllib, urllib2
from django.conf import settings
from common import *
import simplejson

def add_activity(request):
    recdata = request.POST.copy()
    data_urlencode = urllib.urlencode(recdata)
    url = "%s/add_act?" % settings.GM_URL
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
    resdata = {
    "ret":res["ret"],
    "msg":res["msg"],
    }

    ctxt = RequestContext(request,resdata)

    return render_to_response("result.html", ctxt)

def get_activity(request):
    recdata = request.POST.copy()
    data_urlencode = urllib.urlencode(recdata)
    url = "%s/add_act?" % settings.GM_URL
    url_get = url + data_urlencode
    req = urllib2.Request(url_get)
    response = urllib2.urlopen(req)
    a = response.read()
    print "response:",a, type(a)
    res = simplejson.loads(a)
    if not res.has_key("data"):
        res["data"] = []
    resdata = {
    "ret":res["ret"],
    "msg":res["msg"],
    "activities":res["data"],
    }

    ctxt = RequestContext(request,resdata)

    return render_to_response("result.html", ctxt)
