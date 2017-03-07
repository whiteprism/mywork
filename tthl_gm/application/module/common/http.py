# -*- coding:utf-8 -*-
from django.http import HttpResponse
import simplejson

def HttpResponseJson(data):
    return HttpResponse(simplejson.dumps(data), content_type='application/json')
