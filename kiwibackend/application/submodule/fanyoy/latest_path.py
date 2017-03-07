# -*- coding: utf-8 -*-

from tokyotyrant import get_client

from opensocial.templatetags.osmobile import opensocial_url_convert

KVS_LATEST_PATH_FORMAT = u'LatestPath::%s::%s'
def set_latest_path(request, key='default'):
    key = KVS_LATEST_PATH_FORMAT % (request.osuser.pk, key)
    tt_client = get_client('default')
    tt_client.set(key, request.path)

def get_latest_path(request, key='default'):
    key = KVS_LATEST_PATH_FORMAT % (request.osuser.pk, key)
    tt_client = get_client('default')
    latest_path = tt_client.get(key)
    if not latest_path:
        return None
    return opensocial_url_convert(latest_path)

def delete_latest_path(request, key='default'):
    key = KVS_LATEST_PATH_FORMAT % (request.osuser.pk, key)
    tt_client = get_client('default')
    #tt_client.set(key, None)
    tt_client.out(key)

def get_page_url(request):
    return opensocial_url_convert(request.path)
