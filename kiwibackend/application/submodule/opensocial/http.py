# -*- encoding: utf-8 -*-
import simplejson
from django.http import HttpResponse

def HttpResponseJson(data):
    return HttpResponse(simplejson.dumps(data), content_type='application/json')
