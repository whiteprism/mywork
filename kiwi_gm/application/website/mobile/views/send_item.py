# -*- coding: utf-8 -*
from django.contrib.admin.views.decorators import  staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from gameconfig.api import get_models, get_model,check_func
import urllib, urllib2
import simplejson
from module.server.api import get_server_by_request

def send(request):
    '''
    发放物品
    '''
    server = get_server_by_request(request)
    data = dict(request.POST.items())
    data["severId"] = server.id
    data_urlencode = urllib.urlencode(data)
    url = "%s/gmapi/send/send/?" % server.gm_url
    url_get = url + data_urlencode
    req = urllib2.Request(url_get)
    response = urllib2.urlopen(req)
    res = simplejson.loads(response.read())
    resdata = {
    "ret":res["success"],
    "msg":res["message"],
    }

    ctxt = RequestContext(request,resdata)
    return render_to_response("result.html", ctxt)

def delete(request):
    '''
    删除玩家物品
    '''
    server = get_server_by_request(request)
    data = dict(request.POST.items())
    data["severId"] = server.id
    data_urlencode = urllib.urlencode(data)
    url = "%s/gmapi/send/delete/?" % server.gm_url
    url_get = url + data_urlencode
    req = urllib2.Request(url_get)
    response = urllib2.urlopen(req)
    res = simplejson.loads(response.read())
    resdata = {
    "ret":res["success"],
    "msg":res["message"],
    }

    ctxt = RequestContext(request,resdata)
    return render_to_response("result.html", ctxt)

def sends(request):
    '''
    发放物品
    '''
    server = get_server_by_request(request)
    data = dict(request.POST.items())
    data["severId"] = server.id
    data_urlencode = urllib.urlencode(data)
    url = "%s/gmapi/send/sends/?" % server.gm_url
    url_get = url + data_urlencode
    req = urllib2.Request(url_get)
    response = urllib2.urlopen(req)
    res = simplejson.loads(response.read())
    resdata = {
    # "ret":res["success"],
    # "msg":res["message"],
    "data":res
    }

    ctxt = RequestContext(request,resdata)
    return render_to_response("result.html", ctxt)

def deletes(request):
    '''
    删除玩家物品
    '''
    server = get_server_by_request(request)
    data = dict(request.POST.items())
    data["severId"] = server.id
    data_urlencode = urllib.urlencode(data)
    url = "%s/gmapi/send/deletes/?" % server.gm_url
    url_get = url + data_urlencode
    req = urllib2.Request(url_get)
    response = urllib2.urlopen(req)
    res = simplejson.loads(response.read())
    resdata = {
    # "ret":res["success"],
    # "msg":res["message"],
    "data":res
    }

    ctxt = RequestContext(request,resdata)
    return render_to_response("result.html", ctxt)

