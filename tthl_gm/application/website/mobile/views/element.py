# -*- coding: utf-8 -*
from django.contrib.admin.views.decorators import  staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext
import urllib, urllib2
from django.conf import settings
from common import *
import simplejson
from servers.api import get_server_by_request

# @staff_member_required
# def search_element(request):
#     data = request.POST.copy()
#     server = get_server_by_request(request)
#     data["server_id"] = server.id
#     item_type = request.POST.get("element_type")
#     data_urlencode = urllib.urlencode(data)
#     url = "%s/player_property_search?" % server.gm_url
#     url_get = url + data_urlencode
#     result,dt = url_request_handler(url_get)
#     if result:
#         response = dt
#     else:
#         msg_dict = dt
#         ctxt = RequestContext(request,msg_dict)
#         return render_to_response("error.html", ctxt)
#     a = response.read()
#     print "response:",a, type(a)
#     res = simplejson.loads(a)
#     if not res.has_key("data"):
#         res["data"] = []
#     tt = [
#         {
#             "item_type" : "item",
#             "item_id":  1,
#             "item_num": 10,     
#             },
#         {
#             "item_type" : "item",
#             "item_id":  1,
#             "item_num": 10,        
#         },
#         {
#             "item_type" : "item",
#             "item_id":  1,
#             "item_num": 10,         
#         },
#     ]
#     resdata = {
#     "item_type":item_type,
#     "ret":res["ret"],
#     "msg":res["msg"],
#     "properties":tt,
#     }
#     print resdata
#     ctxt = RequestContext(request,resdata)

@staff_member_required
def search_element(request):
    data = request.POST.copy()
    #server = get_server_by_request(request)
    data["server_id"] = 4
    item_type = request.POST.get("element_type")
    # data_urlencode = urllib.urlencode(data)
    # url = "%s/player_property_search?" % settings.GM_URL
    # url_get = url + data_urlencode
    # result,dt = url_request_handler(url_get)
    # if result:
    #     response = dt
    # else:
    #     msg_dict = dt
    #     ctxt = RequestContext(request,msg_dict)
    #     return render_to_response("error.html", ctxt)
    # a = response.read()
    # print "response:",a, type(a)
    # res = simplejson.loads(a)
    # if not res.has_key("data"):
    #     res["data"] = []
    tt = [
        {
            "item_type" : 3,
            "item_id":  1,
            "item_num": 10,     
            },
        {
            "item_type" : 3,
            "item_id":  2,
            "item_num": 10,        
        },
        {
            "item_type" : 3,
            "item_id":  3,
            "item_num": 10,         
        },
    ]
    resdata = {
    "serverid":1,
    "playerid":1,
    "item_type":item_type,
    "ret":0,
    "msg":"tt",
    "properties":tt,
    }
    print resdata
    ctxt = RequestContext(request,resdata)

    return render_to_response("element/search_element.html", ctxt)


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

    return render_to_response("result.html")
