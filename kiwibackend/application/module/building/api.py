# -*- coding: utf-8 -*-
from building.models import Building, BuildingGolden, BuildingUpgrade, BuildingUpgradeCost, BuildingProduction, BuildingProductionCost, BuildingResourceProtected,BuildingRadar,BuildingGoldHand,BuildingFragment,BuildingAttribute, BuildingPlant
import random
def update_building_cache():
    Building.create_cache()
    BuildingGolden.create_cache()
    #BuildingPopulation.create_cache()
    BuildingProduction.create_cache()
    BuildingProductionCost.create_cache()
    BuildingUpgrade.create_cache()
    BuildingUpgradeCost.create_cache()
    BuildingResourceProtected.create_cache()
    BuildingRadar.create_cache()
    BuildingGoldHand.create_cache()
    BuildingFragment.create_cache()
    BuildingAttribute.create_cache()
    BuildingPlant.create_cache()

def get_building(pk):
    return Building.get(int(pk))
#
def get_buildings():
    return Building.get_all_list()

def get_building_upgrade_by_building_and_level(building, level):
    """
    获取建筑升级信息
    """
    building_upgrades = BuildingUpgrade.get_buildingupgrade_by_building(building)
    building_upgrade = None
    for i in building_upgrades:
        if i.level == level:
            building_upgrade = i
            break
    return building_upgrade
    

def get_building_count_by_level(building, level):
    """
    根据等级和等级信息获取建造数量配置
    """

    count = 0
    levelCount = building.levelCount

    for i in range(0, len(levelCount), 2):
        if level >= levelCount[i]:
            count = levelCount[i+1]
        else:
            break

    return count

def get_buildingproductions_by_building(building):
    """
    获取生产兵消耗时间
    """
    return BuildingProduction.get_buildingproduction_by_building(building)
    
#def get_buildingpopulation_by_building(building):
#    """
#    获取人口配置
#    """
#    return BuildingPopulation.get_buildingpopulation_by_building(building)

def get_buildingresourceprotecteds():
    return BuildingResourceProtected.get_all_list()

def get_buildingresourceprotected(building_id, level):
    return BuildingResourceProtected.get(int(building_id * 100 + level))

def get_buildingradars():
    return BuildingRadar.get_all_list()

def get_buildingradar(building_id, level):
    return BuildingRadar.get(int (building_id * 100 + 1))

def get_buildinggoldhands():
    return BuildingGoldHand.get_all_list()

def get_buildinggoldhand(id):
    return BuildingGoldHand.get(int(id))

def get_buildingfragment(pk):
    return BuildingFragment.get(int(pk))

def get_buildingfragments():
    return BuildingFragment.get_all_list()
    
def get_buildingattribute(pk):
    return BuildingAttribute.get(int(pk))

def get_buildingplant_by_buildingid(pk):
    building = get_building(pk)
    return BuildingPlant.get(int(building.buildingPlantId))
 
def get_buildingplant(pk):
    return BuildingPlant.get(int(pk))

def get_buildingplants():
    return BuildingPlant.get_all_list()