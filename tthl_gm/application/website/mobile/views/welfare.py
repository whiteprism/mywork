# -*- coding: utf-8 -*
from django.contrib.admin.views.decorators import  staff_member_required
from django.shortcuts import render_to_response
import urllib, urllib2
from django.conf import settings

@staff_member_required
def send_welfare(request):
    data = request.POST.copy()
    data_urlencode = urllib.urlencode(data)
    url = "%s/send_property?" % settings.GM_URL
    url_get = url + data_urlencode
    result,dt = url_request_handler(url_get)
    if result:
        response = dt
    else:
        msg_dict = dt
        ctxt = RequestContext(request,msg_dict)
        return render_to_response("error.html", ctxt)
    a = response.read()
    res = simplejson.loads(a)
    resdata = {
    "ret":res["ret"],
    "msg":res["msg"],
    }

    ctxt = RequestContext(request,resdata)

    return render_to_response("result.html")
