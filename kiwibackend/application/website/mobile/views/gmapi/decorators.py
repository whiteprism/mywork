# -*- encoding:utf8 -*-
from opensocial.http import HttpResponseJson


WHITELIST = [
    '192.168.2.212',
    '192.168.1.58',
    '192.168.1.72',
]

def handle_verification(view_func):
    def _handle(request):
        print "***",request.META
        ip = request.META.get("REMOTE_ADDR", "")
        print ip
        if ip not in WHITELIST:
            return HttpResponseJson({})
        return view_func(request)
    return _handle
