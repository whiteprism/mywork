# -*- coding: utf-8 -*
from django.contrib.admin.views.decorators import  staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext
import urllib, urllib2
import simplejson
from django.conf import settings
from common import *
from servers.api import get_server_by_request

@staff_member_required
def search_server(request):
    data = request.POST.copy()
    print data
    server = get_server_by_request(request)
    data["server_id"] = server.id
    data_urlencode = urllib.urlencode(data)
    url = "%s/check_server_info_timezone?" % server.gm_url
    url_get = url + data_urlencode
    print url_get
    result,dt = url_request_handler(url_get)
    if result:
        response = dt
    else:
        msg_dict = dt
        ctxt = RequestContext(request,msg_dict)
        return render_to_response("error.html", ctxt)
    a = response.read()
    res = simplejson.loads(a)
    print res
    if not res.has_key("data"):
        res["data"] = []
    for data in res["data"]:
        dic = data["level_array"]
        lis = sorted(dic.keys())
        for key in lis:
            if not dic.has_key(str(i)):
                dic[str(i)] = 0
            lis.append(dic[str(i)])
        data["level_array"] = lis
    resdata = {
    "ret":res["ret"],
    "msg":res["msg"],
    "serverinfos":res["data"]
    }

    ctxt = RequestContext(request,resdata)

    return render_to_response("server/info_with_timezone.html", ctxt)

@staff_member_required
def search_server_notime(request):
    data = request.POST.copy()
    data_urlencode = urllib.urlencode(data)
    url = "%s/check_server_info?" % server.gm_url
    url_get = url + data_urlencode
    print url_get
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
    "serverinfos":res["data"]
    }

    ctxt = RequestContext(request,resdata)

    return render_to_response("server/info_notime.html", ctxt)
