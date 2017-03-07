# -*- coding: utf-8 -*-
from mysteryshop.models import MysteryShop,MysteryShopGrid

def update_mysteryshop_cache():
    MysteryShop.create_cache()
    MysteryShopGrid.create_cache()

def get_mysteryshop(pk):
    return MysteryShop.get(int(pk))

def get_mysteryshops():
    return MysteryShop.get_all_list()

def get_mysteryshopgrids():
    return MysteryShopGrid.get_all_list()

def get_mystershopitems_by_show_id(show_id):
    return MysteryShop.get_items_by_show_id(show_id)
