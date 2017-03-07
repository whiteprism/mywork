# -*- coding: utf-8 -*-
import md5
from django.conf import settings
import time
from common.http import HttpSdkResponseJson
from common.static import HTTPCode
from gameconfig.api import get_game, get_channel
import simplejson
import urllib

def _get_sign_parameters_str(params, span_with="", with_quote=False):
    """Return a string that contains the parameters that must be signed."""
    key_values = []
    for k, v in params.iteritems():
        key_values.append((k,v))
    # Sort lexicographically, first after key, then after value.
    key_values.sort()
    # Combine kpairs into a string.
    if with_quote:
        return span_with.join(['%s=%s' % (k, urllib.quote_plus(str(v))) for k, v in key_values])
    else:
        return span_with.join(['%s=%s' % (k, v) for k, v in key_values])

def _get_sign_parameters_str_with_span(params, span1_with="", span2_with=""):
    """Return a string that contains the parameters that must be signed."""
    key_values = []
    for k, v in params.iteritems():
        key_values.append((k,v))
    # Sort lexicographically, first after key, then after value.
    key_values.sort()
    # Combine key value pairs into a string.
    return span2_with.join(['%s%s%s' % (k, span1_with, v) for k, v in key_values])

def generate_sign(params, game):
    """
    验证加密串
    """
    sign_str = _get_sign_parameters_str(params, span_with="&")
    sign_str = "%s%s" % (sign_str, game.secretKey) 
    print sign_str
    return md5.md5(sign_str).hexdigest()

#逻辑服务器验证用户id是否正确
def generate_token(params, game):
    """
    生成令牌
    """
    sign_str = _get_sign_parameters_str(params, span_with="&")
    sign_str = "token:s%s" % (sign_str, game.secretKey) 
    return md5.md5(sign_str).hexdigest()

def secret_verification(view_func):                                    
    def decorate(request, *args, **kwds):                              
        game_id = request.POST.get('gameId', '').strip() 
        channel_id = request.POST.get('channelId', '').strip() 
        t = request.POST.get('t', '').strip() 

        game = get_game(game_id)
        channel = get_channel(channel_id)
        request.game = game
        request.channel = channel
        print dict(request.POST.items())

        if not game:
            response = HttpSdkResponseJson(request, HTTPCode.ERROR_GAME_NONE)
        elif not channel:
            response = HttpSdkResponseJson(request, HTTPCode.ERROR_CHANNEL_NONE)
        elif not t:
            response = HttpSdkResponseJson(request, HTTPCode.ERROR)
        else:
            data = dict(request.POST.items())
            sign =  data["sign"]
            del data["sign"]
            backSign = generate_sign(data, game)
            if sign != backSign:
                response = HttpSdkResponseJson(request, HTTPCode.ERROR_SIGN)
            else:
                response =  view_func(request, *args, **kwds)                       
        response["Access-Control-Allow-Origin"] =  "*" 
        response["Access-Control-Allow-Headers"] =  "*"
        return response
    return decorate
