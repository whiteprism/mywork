# -*- coding: utf-8 -*
from django.contrib.admin.views.decorators import  staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext
import urllib, urllib2
from django.conf import settings

@staff_member_required
def search_order():
    data = request.POST.copy()
    data_urlencode = urllib.urlencode(data)
    url = "%s/order_search?" % settings.GM_URL
    url_get = url + data_urlencode
    result,dt = url_request_handler(url_get)
    if result:
        response = dt
    else:
        msg_dict = dt
        ctxt = RequestContext(request,msg_dict)
        return render_to_response("error.html", ctxt)
    res = simplejson.loads(response.read())
    if res.has_key("data"):
        resdata = {
        "serverid":data["server_id"],
        "orderid":data["order_id"],
        "ret":res["ret"],
        "msg":res["msg"],
        "playerinfos":res["data"]
        }

        ctxt = RequestContext(request,resdata)
        return render_to_response("order/search_order.html", ctxt)
    else:
        return render_to_response("data_not_found.html")

@staff_member_required
def add_order(request):
    data = request.POST.copy()
    data_urlencode = urllib.urlencode(data)
    url = "%s/add_order?" % settings.GM_URL
    url_get = url + data_urlencode
    result,dt = url_request_handler(url_get)
    if result:
        response = dt
    else:
        msg_dict = dt
        ctxt = RequestContext(request,msg_dict)
        return render_to_response("error.html", ctxt)
    res = simplejson.loads(response.read())
    resdata = {
    "ret":res["ret"],
    "msg":res["msg"],
    }
    ctxt = RequestContext(request,resdata)
    return render_to_response("result.html")

@staff_member_required
def fake_order(request):
    data = request.POST.copy()
    data_urlencode = urllib.urlencode(data)
    url = "%s/fake_order?" % settings.GM_URL
    url_get = url + data_urlencode
    result,dt = url_request_handler(url_get)
    if result:
        response = dt
    else:
        msg_dict = dt
        ctxt = RequestContext(request,msg_dict)
        return render_to_response("error.html", ctxt)
    res = simplejson.loads(response.read())
    resdata = {
    "ret":res["ret"],
    "msg":res["msg"],
    }
    ctxt = RequestContext(request,resdata)
    return render_to_response("result.html")

