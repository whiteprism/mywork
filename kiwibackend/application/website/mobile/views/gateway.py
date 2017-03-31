# -*- coding: utf-8 -*-
import msgpack
from django.http import HttpResponse
from custom_urls import custom_controller
from messages.http.message import MessageRequest, MessageResponse

def index(request):
    content_len = request.META.get("CONTENT_LENGTH",0)
    content_len = int(content_len) if content_len else 0
    request_body = request.META['wsgi.input'].read(content_len)

    if content_len > 0:

        contents = msgpack.unpackb(request_body)
        yoyprint(contents)
        message_request = MessageRequest()
        message_response = MessageResponse()
        message_request.http_request = request

        request.message_request = message_request
        request.message_response = message_response

        message_request.for_request(contents)
        message_response.set("messageId",message_request.messageId)
        yoyprint(u"message id is %s" % message_request.messageId)

        print message_request.messageId

        custom_view = custom_controller(message_request.messageId)

        message_request.view_name = custom_view["name"]
        message_request.request_body = request_body

        message_response = custom_view["view"](message_request, message_response)


        if message_request.view_name != "init":
           yoyprint(message_response.for_response())

        return HttpResponse(msgpack.packb(message_response.for_response()))
    else:
        return HttpResponse("SOS...") 
