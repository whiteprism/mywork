# -*- coding: utf-8 -*-
from item.models import Item, Store, ItemCompose, CouragePointStore, TowerStore

def update_item_cache():
    Item.create_cache()
    Store.create_cache()
    ItemCompose.create_cache()
    CouragePointStore.create_cache()
    TowerStore.create_cache()

def get_item(pk):
    return Item.get(int(pk))

def get_items():
    return Item.get_all_list()

def get_storeitem(pk):
    return Store.get(int(pk))

def get_storeitems():
    return Store.get_all_list()

def get_itemcomposes():
    return ItemCompose.get_all_list()

def get_itemcomposes_by_item_id(item_id):
    return ItemCompose.get_itemcomposes_by_item_id(item_id)

def get_couragepointstore(pk):
    return CouragePointStore.get(int(pk))

def get_couragepointstores():
    return CouragePointStore.get_all_list()

def get_towerstore(pk):
    return TowerStore.get(int(pk))

def get_towerstores():
    return TowerStore.get_all_list()
