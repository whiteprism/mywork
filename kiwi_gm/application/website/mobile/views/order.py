# -*- coding: utf-8 -*
from django.contrib.admin.views.decorators import  staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext
import urllib, urllib2
from module.server.api import get_server_by_request
import simplejson
from common import *

@staff_member_required
def by_user(request):
    '''
    通过玩家ID查询订单
    '''
    server = get_server_by_request(request)
    data = dict(request.POST.items())
    data["severId"] = server.id
    #data["playerId"] = ','.join(data["playerId"].split("\r\n"))
    data_urlencode = urllib.urlencode(data)
    url = "%s/gmapi/order/player/?" % server.gm_url
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
    "ret":res["success"],
    "msg":res["message"],
    "orders":res["data"],
    }

    ctxt = RequestContext(request,resdata)
    return render_to_response("order/search_result.html", ctxt)

@staff_member_required
def by_order(request):
    '''
    通过订单号查询订单
    '''
    server = get_server_by_request(request)
    data = dict(request.POST.items())
    data["severId"] = server.id
    #data["playerId"] = ','.join(data["playerId"].split("\r\n"))
    data_urlencode = urllib.urlencode(data)
    url = "%s/gmapi/order/orderid/?" % server.gm_url
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
    "ret":res["success"],
    "msg":res["message"],
    "orders":res["data"],
    }

    ctxt = RequestContext(request,resdata)
    return render_to_response("order/search_result.html", ctxt)

@staff_member_required
def by_plat(request):
    '''
    通过平台单号查询订单
    '''
    server = get_server_by_request(request)
    data = dict(request.POST.items())
    data["severId"] = server.id
    #data["playerId"] = ','.join(data["playerId"].split("\r\n"))
    data_urlencode = urllib.urlencode(data)
    print data_urlencode
    url = "%s/gmapi/order/plat/orderid/?" % server.gm_url
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
    "ret":res["success"],
    "msg":res["message"],
    "orders":res["data"],
    }

    ctxt = RequestContext(request,resdata)
    return render_to_response("order/search_result.html", ctxt)

@staff_member_required
def by_time(request):
    '''
    通过时间查询订单
    '''
    server = get_server_by_request(request)
    data = dict(request.POST.items())
    data["severId"] = server.id
    #data["playerId"] = ','.join(data["playerId"].split("\r\n"))
    data_urlencode = urllib.urlencode(data)
    url = "%s/gmapi/order/time/?" % server.gm_url
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
    "ret":res["success"],
    "msg":res["message"],
    "orders":res["data"],
    }

    ctxt = RequestContext(request,resdata)
    return render_to_response("order/search_result.html", ctxt)

@staff_member_required
def rank(request):
    '''
    查看充值排名
    '''
    server = get_server_by_request(request)
    data = dict(request.POST.items())
    data["severId"] = server.id
    #data["playerId"] = ','.join(data["playerId"].split("\r\n"))
    data_urlencode = urllib.urlencode(data)
    print data_urlencode
    url = "%s/gmapi/order/rank/?" % server.gm_url
    url_get = url + data_urlencode
    result,dt = url_request_handler(url_get)
    if result:
        response = dt
    else:
        msg_dict = dt
        ctxt = RequestContext(request,msg_dict)
        return render_to_response("error.html", ctxt)
    res = simplejson.loads(response.read())
    print res
    resdata = {
    "ret":res["success"],
    "msg":res["message"],
    "ranks":res["data"],
    }

    ctxt = RequestContext(request,resdata)
    return render_to_response("order/rank_result.html", ctxt)

@staff_member_required
def search_order():
    data = request.POST.copy()
    data_urlencode = urllib.urlencode(data)
    url = "%s/order_search?" % real_url
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
    url = "%s/add_order?" % real_url
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
    return render_to_response("result.html")

@staff_member_required
def fake_order(request):
    data = request.POST.copy()
    data_urlencode = urllib.urlencode(data)
    url = "%s/fake_order?" % real_url
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
    return render_to_response("result.html")

