# -*- coding: utf-8 -*-
from module.utils import is_digits
from building.models import Building, BuildingFragment
from module.building.api import get_building
from .docs import PlayerBuilding
from module.common.actionlog import ActionLogWriter

def acquire_building(player, building_or_building_id, info="", **argvs):
    ''' 
    获取建筑
    '''
    if isinstance(building_or_building_id, Building):
        building = building_or_building_id
    elif is_digits(building_or_building_id):
        building = get_building(building_or_building_id)
        if not building:
            return None
    else:
        return None
        
    playerbuilding = player.buildings.create(pk=PlayerBuilding._incrment_id(), building_id = building.pk, **argvs)
    player.update_building(playerbuilding, True)
    ActionLogWriter.building_create(player, playerbuilding.pk, playerbuilding.building_id, info)
    return playerbuilding
    
def acquire_buildingfragment(player, fragment_or_fragment_id, number=1, info="", **argvs):
    """
    获取建筑碎片
    """
    if isinstance(fragment_or_fragment_id, BuildingFragment):
        buildingfragment_id = fragment_or_fragment_id.pk
    elif is_digits(int(fragment_or_fragment_id)):
        buildingfragment_id = int(fragment_or_fragment_id)

    _, playerbuildingfragment = player.buildingfragments.get_or_create(buildingfragment_id, obj_id=buildingfragment_id, **argvs)
    playerbuildingfragment.add(number, info)
    player.update_buildingfragment(playerbuildingfragment, True)
    return playerbuildingfragment