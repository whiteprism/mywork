# # -*- coding: utf-8 -*-
from django.http import HttpResponse
from module.common.static import ErrorID
import msgpack

def page_500(request):
    request.message_response.common_response.set("success", False)
    request.message_response.common_response.set("errorCode", ErrorID.ERROR_DATA_ERROR)
    return HttpResponse(msgpack.packb(request.message_response.for_response()))
             
def page_404(request):
    return page_500(request)
