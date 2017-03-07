# -*- coding: utf-8 -*-
from icon.models import Icon

def update_icon_cache():
    Icon.create_cache()

def get_icon(pk):
    return Icon.get(int(pk))

def get_icons():
    return Icon.get_all_list()
