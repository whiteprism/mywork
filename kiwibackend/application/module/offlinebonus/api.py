# -*- coding: utf-8 -*-
from offlinebonus.models import OfflineBonusLevel, OfflineBonusDay

def update_offlinebonus_cache():
    OfflineBonusLevel.create_cache()
    OfflineBonusDays.create_cache()

def get_offlinebonuslevels():
    return OfflineBonusLevel.get_all_list()

def get_offlinebonusdays():
    return OfflineBonusDay.get_all_list()

def get_offlinebonuslevel(pk):
    return OfflineBonusLevel.get(pk)

def get_offlinebonusday(pk):
    return OfflineBonusDay.get(pk)
