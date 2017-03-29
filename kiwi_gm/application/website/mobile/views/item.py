# -*- coding: utf-8 -*
from django.contrib.admin.views.decorators import  staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from gameconfig.api import get_models, get_model,check_func
import urllib, urllib2
import simplejson
from module.server.api import get_server_by_request
from common import *

@staff_member_required
def query(request):
    '''
    查看玩家物品
    '''
    server = get_server_by_request(request)
    userID = request.POST.get("playerId")
    data = dict(request.POST.items())
    server = get_server_by_request(request)
    data["severId"] = server.id
    data_urlencode = urllib.urlencode(data)
    print data_urlencode
    print server.id
    if data["type"] == "hero":
        return query_hero(request,data_urlencode,server.gm_url)
    elif data["type"] == "item":
        return query_item(request,data_urlencode,server.gm_url)
    elif data["type"] == "equip":
        return query_equip(request,data_urlencode,server.gm_url)
    elif data["type"] == "equipfragment":
        return query_equipfragment(request,data_urlencode,server.gm_url)
    elif data["type"] == "artifact":
        return query_artifact(request,data_urlencode,server.gm_url)
    elif data["type"] == "artifactfragment":
        return query_artifactfragment(request,data_urlencode,server.gm_url)
    elif data["type"] == "building":
        return query_building(request,data_urlencode,server.gm_url)
    elif data["type"] == "buildingfragment":
        return query_buildingfragment(request,data_urlencode,server.gm_url)
    elif data["type"] == "plant":
        return query_plant(request,data_urlencode,server.gm_url)
    elif data["type"] == "soulfragment":
        return query_soulfragment(request,data_urlencode,server.gm_url)
    elif data["type"] == "pve":
        return query_pve(request,data_urlencode,server.gm_url)
    elif data["type"] == "elementtower":
        return query_elementtower(request,data_urlencode,server.gm_url)
    else:
        return HttpResponse(u"请求信息不足！",content_type='text/plain')

def query_hero(request,reqdata,real_url):
    '''
    查看玩家英雄
    '''
    print "***"
    url = "%s/gmapi/hero/query/?" % real_url
    url_get = url + reqdata
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
    "heros":res["data"],
    }
    ctxt = RequestContext(request,resdata)
    return render_to_response("property/hero_result.html",ctxt)

def query_item(request,reqdata,real_url):
    '''
    查看玩家物品
    '''
    url = "%s/gmapi/item/query/?" % real_url
    url_get = url + reqdata
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
    "heros":res["data"],
    }
    ctxt = RequestContext(request,resdata)
    return render_to_response("property/item_result.html",ctxt)

def query_equip(request,reqdata,real_url):
    '''
    查看玩家装备
    '''
    url = "%s/gmapi/equip/query/?" % real_url
    url_get = url + reqdata
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
    "equips":res["data"],
    }
    ctxt = RequestContext(request,resdata)
    return render_to_response("property/equip_result.html",ctxt)

def query_equipfragment(request,reqdata,real_url):
    '''
    查看玩家装备碎片
    '''
    url = "%s/gmapi/equipfragment/query/?" % real_url
    url_get = url + reqdata
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
    "equipfragments":res["data"],
    }
    ctxt = RequestContext(request,resdata)
    return render_to_response("property/equipfragment_result.html",ctxt)

def query_artifact(request,reqdata,real_url):
    '''
    查看玩家圣物
    '''
    url = "%s/gmapi/artifact/query/?" % real_url
    url_get = url + reqdata
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
    "artifacts":res["data"],
    }
    ctxt = RequestContext(request,resdata)
    return render_to_response("property/artifact_result.html",ctxt)

def query_artifactfragment(request,reqdata,real_url):
    '''
    查看玩家圣物碎片
    '''
    url = "%s/gmapi/artifactfragment/query/?" % real_url
    url_get = url + reqdata
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
    "artifactfragments":res["data"],
    }
    ctxt = RequestContext(request,resdata)
    return render_to_response("property/artifactfragment_result.html",ctxt)

def query_building(request,reqdata,real_url):
    '''
    查看玩家建筑
    '''
    url = "%s/gmapi/building/query/?" % real_url
    url_get = url + reqdata
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
    "buildings":res["data"],
    }
    ctxt = RequestContext(request,resdata)
    return render_to_response("property/building_result.html",ctxt)

def query_buildingfragment(request,reqdata,real_url):
    '''
    查看玩家建筑碎片
    '''
    url = "%s/gmapi/buildingfragment/query/?" % real_url
    url_get = url + reqdata
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
    "buildingfragments":res["data"],
    }
    ctxt = RequestContext(request,resdata)
    return render_to_response("property/buildingfragment_result.html",ctxt)

def query_plant(request,reqdata,real_url):
    '''
    查看玩家植物
    '''
    url = "%s/gmapi/buildingplant/query/?" % real_url
    url_get = url + reqdata
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
    "plants":res["data"],
    }
    ctxt = RequestContext(request,resdata)
    return render_to_response("property/plant_result.html",ctxt)

def query_soulfragment(request,reqdata,real_url):
    '''
    查看玩家灵魂碎片
    '''
    url = "%s/gmapi/soul/query/?" % real_url
    url_get = url + reqdata
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
    "soulfragments":res["data"],
    }
    ctxt = RequestContext(request,resdata)
    return render_to_response("property/soulfragment_result.html",ctxt)

def query_pve(request,reqdata,real_url):
    '''
    查看玩家副本
    '''
    url = "%s/gmapi/instance/race/?" % real_url
    url_get = url + reqdata
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
    "pves":res["data"],
    }
    ctxt = RequestContext(request,resdata)
    return render_to_response("property/pve_result.html",ctxt)

def query_elementtower(request,reqdata,real_url):
    '''
    查看玩家元素之塔
    '''
    url = "%s/gmapi/instance/elementtower/?" % real_url
    url_get = url + reqdata
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
    "elementtower":res["data"],
    }
    ctxt = RequestContext(request,resdata)
    return render_to_response("property/elementtower_result.html",ctxt)
