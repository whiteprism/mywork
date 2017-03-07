# -*- coding: utf-8 -*-
from module.utils import is_digits
from building.models import BuildingPlant
from module.building.api import get_buildingplant
from .docs import PlayerPlant

def acquire_buildingplant(player, plant_id, info="", **argvs):
    ''' 
    获取建筑
    '''
    if isinstance(plant_id, BuildingPlant):
        plant = plant_id
    elif is_digits(plant_id):
        plant = get_buildingplant(plant_id)
        if not plant:
            return None
    else:
        return None
        
    playerplant = player.buildingplants.create(pk = PlayerPlant._incrment_id(), plantId = plant.pk, **argvs)
    #设置种植时间
    playerplant.cultivate()
    player.update_buildingplant(playerplant, True)
    return playerplant