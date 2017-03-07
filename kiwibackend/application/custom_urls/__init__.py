# -*- coding:utf8 -*-

from urls import custom_urls
__all__ = ["custom_controller"]

#{1:{"view":website.mobile.views.index.root,"name":"login"}}
custom_views = dict(custom_urls)

def custom_controller(action):
    return custom_views.get(action, None)
