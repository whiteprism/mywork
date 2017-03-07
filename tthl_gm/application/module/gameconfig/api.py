# -*- coding: utf-8 -*-

from gameconfig.models import *

def get_gameauth(request):
    """
    获取当前用户
    """
    return GameAuth.objects.get(user=request.user)

def get_models(request):
    """
    获取当前用户所有模块配置
    """
    gameauth = get_gameauth(request)
    models = GameModel.objects.filter(secret_level__lte=gameauth.secret_level).order_by("sort")
    return models


def get_model(request, modelID):
    """
    获取当前用户
    """
    gameauth = get_gameauth(request)
    try:
        m = GameModel.objects.get(pk=int(modelID))
    except:
        m = None
    return m

def check_func(request, funcID):
    """
    获取当前用户
    """
    gameauth = get_gameauth(request)
    try:
        f = GameFunc.objects.get(pk=int(funcID))
    except:
        f = None

    if f and gameauth.secret_level >= f.secret_level:
        return True

    return False
