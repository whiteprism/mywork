# -*- coding: utf-8 -*
from django.contrib.admin.views.decorators import  staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext
import urllib, urllib2
from servers.api import get_server_by_request
import simplejson
from django.conf import settings
from common import *

def get_mail(request):
    '''
    查看玩家邮件
    '''
    server = get_server_by_request(request)
    data = dict(request.POST.items())
    data["playerId"] = ','.join(data["playerId"].split("\r\n"))
    data["server_id"] = server.id
    data_urlencode = urllib.urlencode(data)
    print data_urlencode
    url = "%s/get_mail/?" % server.gm_url
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
    "mails":res["data"],
    }

    ctxt = RequestContext(request,resdata)
    return render_to_response("mail/get_result.html", ctxt)

def send_mail(request):
    '''
    发送系统邮件
    '''
    server = get_server_by_request(request)
    #userID = request.POST["playerIdList"]
    data = dict(request.POST.items())
    data["severId"] = server.id
    data["playerIdList"] = ','.join(data["playerIdList"].split("\r\n"))
    data_urlencode = urllib.urlencode(data)
    url = "%s/send_mail/?" % server.gm_url
    url_get = url + data_urlencode
    result,dt = url_request_handler(url_get)
    if result:
        response = dt
    else:
        msg_dict = dt
        ctxt = RequestContext(request,msg_dict)
        return render_to_response("error.html", ctxt)
    res = simplejson.loads(response.read())
    userCount = len(data["playerIdList"].split(","))
    countList = range(1,userCount+1)
    if data["playerIdList"] == "all":
        all = True
    else:
        all = False
    resdata = {
    "all":all,
    "userCount":userCount,
    "data":res
    }

    ctxt = RequestContext(request,resdata)
    return render_to_response("mail/send_result.html", ctxt)
