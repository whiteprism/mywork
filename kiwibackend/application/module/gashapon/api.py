# -*- coding: utf-8 -*-

from gashapon.models import Gashapon, GashaponRarityProbability, GashaponProbability, Tavern,TavernCost 

def update_gashapon_cache():
    GashaponRarityProbability.create_cache()
    GashaponProbability.create_cache()
    Gashapon.create_cache()
    Tavern.create_cache()
    TavernCost.create_cache()

def get_gashapon(pk):
    return Gashapon.get(int(pk))

def get_taverns():
    return Tavern.get_all_list()

def get_tavern(pk):
    return Tavern.get(int(pk))
