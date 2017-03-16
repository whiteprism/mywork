# -*- coding: utf-8 -*
from django.contrib.admin.views.decorators import  staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext
import urllib, urllib2
from django.conf import settings
from common import *
import simplejson

@staff_member_required
def search_element(request):
    data = request.POST.copy()
    print data
    item_type = request.POST.get("element_type")
    data_urlencode = urllib.urlencode(data)
    url = "%s/player_property_search?" % settings.GM_URL
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
        "item_type":item_type,
        "ret":res["ret"],
        "msg":res["msg"],
        "properties":res["data"]
        }

        ctxt = RequestContext(request,resdata)

        return render_to_response("element/search_element.html", ctxt)
    else:
        return render_to_response("data_not_found.html")

@staff_member_required
def delete_element(request):
    data = request.POST.copy()
    data_urlencode = urllib.urlencode(data)
    url = "%s/player_property_delete?" % settings.GM_URL
    url_get = url + data_urlencode
    result,dt = url_request_handler(url_get)
    if result:
        response = dt
    else:
        msg_dict = dt
        ctxt = RequestContext(request,msg_dict)
        return render_to_response("error.html", ctxt)
    res = simplejson.loads(a)
    resdata = {
    "ret":res["ret"],
    "msg":res["msg"],
    }

    ctxt = RequestContext(request,resdata)

    return render_to_response("data_not_found.html")
