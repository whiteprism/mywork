# -*- coding: utf-8 -*-
from pvp.models import PVPRank, PVPReward, PVPScene,PVPUpgradeScore,SiegeRandomNumber
def update_pvp_cache():
    PVPRank.create_cache()
    PVPReward.create_cache()
    PVPScene.create_cache()
    PVPUpgradeScore.create_cache()
    SiegeRandomNumber.create_cache()
    SiegeAttactSoldierInfo.create_cache()

def get_pvpRank(pk):
    return PVPRank.get(int(pk))

def get_pvpRanks():
    return PVPRank.get_all_list()

def get_pvpScenes():
    return PVPScene.get_all_list()

def get_pvpUpgradeScore(pk):
    return PVPUpgradeScore.get(int(pk))

def get_pvpUpgradeScores():
    return PVPUpgradeScore.get_all_list()

# def get_siegeAttactSoldierInfos():
#     return SiegeAttactSoldierInfo.get_all_list()

def get_pvpUpgradeScoreKeys():
    scores = PVPUpgradeScore.get_all_dict()
    keys = scores.keys()
    keys.sort(reverse=True)
    return keys

def get_pvpSiegeRandomNumber(pk):
    return SiegeRandomNumber.get(int(pk))


