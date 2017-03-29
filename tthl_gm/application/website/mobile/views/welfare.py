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
def send_welfare(request):
    print request.POST
    data = request.POST.copy()
    print data
    server = get_server_by_request(request)
    data["server_id"] = server.id
    data_urlencode = urllib.urlencode(data)
    url = "%s/add_item?" % server.gm_url
    url_get = url + data_urlencode
    result,dt = url_request_handler(url_get)
    if result:
        response = dt
    else:
        msg_dict = dt
        ctxt = RequestContext(request,msg_dict)
        return render_to_response("error.html", ctxt)
    a = response.read()
    print a,type(a)
    res = simplejson.loads(a)
    resdata = {
    "ret":res["ret"],
    "msg":res["msg"],
    }

    ctxt = RequestContext(request,resdata)

    return render_to_response("result.html")
