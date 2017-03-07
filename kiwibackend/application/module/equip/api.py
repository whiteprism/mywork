# -*- coding: utf-8 -*-
from equip.models import Equip, EquipAttribute, EquipFragment, EquipEnhance, CardEquipInfo, EquipSuit, EquipSuitAttr, EquipRefine
from common.static import Static

def update_equip_cache():
    Equip.create_cache()
    EquipEnhance.create_cache()
    EquipAttribute.create_cache()
    EquipFragment.create_cache()
    CardEquipInfo.create_cache()
    EquipSuit.create_cache()
    EquipSuitAttr.create_cache()
    EquipRefine.create_cache()

def get_equip(pk):
    return Equip.get(int(pk))

def get_equips():
    return Equip.get_all_list()

def get_cardequip(career_id):
    return CardEquipInfo.get(int(career_id))

def get_equipfragment(pk):
    return EquipFragment.get(int(pk))

def get_equipfragments():
    return EquipFragment.get_all_list()

def get_equipenhances():
    #60级
    return EquipEnhance.get_all_list()

def get_equipenhance(level):
    return EquipEnhance.get(level)

def get_equipattribute(pk):
    return EquipAttribute.get(int(pk))

def get_equipsuits():
    return EquipSuit.get_all_list()

def get_equiprefine(quality, refine_level):
    pk = str(quality *100 + refine_level)
    return EquipRefine.get(int(pk))

def get_equiprefines():
    return EquipRefine.get_all_list()
