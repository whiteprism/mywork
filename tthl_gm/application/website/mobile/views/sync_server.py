# -*- coding: utf-8 -*
from django.contrib.admin.views.decorators import  staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext
import urllib, urllib2
from servers.api import get_servers, delete_server, insert_server
import simplejson

get_server_url = "http://fanyoy.xicp.net:2300/gmapi/server/list/?gameId=kiwi"

@staff_member_required
def sync(request):
    '''
    同步服务器
    '''
    req = urllib2.Request(get_server_url)
    response = urllib2.urlopen(req)
    a = response.read()
    res = simplejson.loads(a)
    print res
    if res["servers"]:
        servers = get_servers()
        for server in servers:
            delete_server(server.id)
        datas = res["servers"]
        for data in datas:
            print data["int_code"]
            insert_server(data)
            print "***"

    servers_show = get_servers()
    print servers_show
    resdata = {
    "servers":servers_show,
    }
    ctxt = RequestContext(request,resdata)
    return render_to_response("model/sync_server.html", ctxt)
