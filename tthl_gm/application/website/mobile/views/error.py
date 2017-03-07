# # -*- coding: utf-8 -*-
from common.http import HttpResponseJson

def page_500(request):
    data = {}
    data['httpCode'] = 500
    return HttpResponseJson(data)

def page_404(request):
    return page_500(request)
