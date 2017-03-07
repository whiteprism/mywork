# -*- coding: utf-8 -*
from django.contrib.admin.views.decorators import  staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from gameconfig.api import get_models, get_model
import urllib, urllib2
from feedback import check_feedback
from module.server.api import get_servers

@staff_member_required
def index(request):
    models = get_models(request)
    servers = get_servers()
    data = {
        "models" : models,
        "servers": servers,
    }
    ctxt = RequestContext(request,data)
    return render_to_response("index.html", ctxt)

@staff_member_required
def model(request):
    modelID = request.POST.get("id")

    data = {}
    model = get_model(request, modelID)

    if not model:
        return render_to_response("error.html")

    #ctxt = RequestContext(request,data)
    if model.tag == "feedback":
        return check_feedback(request,page=1)
    elif model.tag == "sync_server":
        servers = get_servers()
        print servers
        data["servers"] = servers

    ctxt = RequestContext(request,data)
    return render_to_response("model/%s.html" % model.tag, ctxt)

