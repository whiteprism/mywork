# -*- coding: utf-8 -*-
from module.playerequip.api import get_playerhero_equips
from module.playerartifact.api import get_playerhero_artifacts
from module.hero.api import get_warrior_level, get_herostar, get_warrior, get_warriorlevel
from module.common.static import Static

def toIntsInts(data):
    '''
    int[] to int[][]
    '''
    array_list = []
    i = 0
    while i < len(data):
        num = data[i]
        i+=1
        array = data[i:num+i]
        array_list.append(array)
        i+=num
    return array_list

def toInts(array_list):
    '''
    int[] to int[][]
    '''
    array = []
    for i in range(0, len(array_list)):
        temp_list = array_list[i]
        array.append(len(temp_list))
        for i_data in temp_list:
            array.append(int(i_data))
    return array

def toWarriorData(data):
    '''
    将ints[][] to warriorDict_list
    '''
    index = 0
    spellsInfo = []
    equipsInfo = []
    #gemsInfo = []
    artifactInfo = []
    warriorDict_list = []
    while index < len(data):
        w_dict = {}
        array = data[index]
        w_dict["gid"] = array[0]
        w_dict["level"] = array[1]
        w_dict["leftGrid"] = array[2]
        w_dict["topGrid"] = array[3]
        w_dict["serverHp"] = array[4]
        w_dict["serverEnergy"] = array[5]
        w_dict["nodeId"] = array[6]
        w_dict["upgrade"] = array[7]
        w_dict["star"] = array[8]
        w_dict["destinyLevel"] = array[9]
        w_dict["fireBuff"] = array[10]
        index+=1
        w_dict["techIndex"] = data[index]
        index += 1
        #判断英雄
        if int(str(array[0])[0:2]) == 11:
            w_dict["spellsInfo"] = data[index]
            index+=1
            w_dict["equipsInfo"] = data[index]
            index+=1
            #w_dict["gemsInfo"] = data[index]
            w_dict["artifactInfo"] = data[index]
            index+=1
            w_dict["teamInfo"] = data[index]
            index+=1
            w_dict["masterInfo"] = data[index]
            index+=1
            # w_dict["trainInfo"] = data[index]
            # index+=1
        warriorDict_list.append(w_dict)

    return warriorDict_list

    
        
def warriorDataToInts(warriorDict_list):
    '''
    warriorDict_list to ints[][]     
    '''
    array_list = []
    for w_dict in warriorDict_list:
        array = []
        #append顺序不能够更改
        array.append(w_dict["gid"])
        array.append(w_dict["level"])
        if not w_dict["leftGrid"]:
            w_dict["leftGrid"] = 0
        array.append(w_dict["leftGrid"])
        if not w_dict["topGrid"]:
            w_dict["topGrid"] = 0
        array.append(w_dict["topGrid"])
        array.append(w_dict["serverHp"])
        array.append(w_dict["serverEnergy"])
        array.append(w_dict["nodeId"])
        array.append(w_dict["upgrade"])
        array.append(w_dict["star"])
        array.append(w_dict["destinyLevel"])
        array.append(w_dict["fireBuff"])

        array_list.append(array)
        array_list.append(w_dict["techIndex"])
        #判断英雄
        if int(str(array[0])[0:2]) == 11:
            array_list.append(w_dict["spellsInfo"])
            array_list.append(w_dict["equipsInfo"])
            array_list.append(w_dict["artifactInfo"])
            array_list.append(w_dict["teamInfo"])
            array_list.append(w_dict["masterInfo"])
          #  array_list.append(w_dict["trainInfo"])

    return array_list

def toTechData(data):
    '''
    ints[][] to techDict_list
    '''
    index = 0
    techDict_list = []
    #print "tech data [][] is :", data
    while index < len(data):
        t_dict = {}
        array = data[index]
        index+=1
        if array:
            t_dict["target"] = array[0]
            t_dict["abilityType"] = array[1]
            t_dict["value"] = array[2]
            techDict_list.append(t_dict)
    return techDict_list

def techDataToInts(teches):
    '''
    techDict to ints[][]     
    '''
    array_list = []

    for t_dict in teches:
        array = []
        #append顺序不能够更改
        array.append(t_dict["target"])
        array.append(t_dict["abilityType"])
        array.append(t_dict["value"])
        array_list.append(array)

    return array_list


def get_warrior_and_tech_dict_list_by_army_data(army_data):
    '''
    通过army_data数据回去warrior数据的字典
    '''

    data_list = toIntsInts(army_data)

    data = toIntsInts(data_list[0])#warrior
    data2 = toIntsInts(data_list[1]) # tech

    warrior_dict_list = toWarriorData(data)
    tech_dict_list = toTechData(data2)


    return warrior_dict_list, tech_dict_list
    
def get_army_data_by_warrior_dict_list(warriors, teches):
    '''
    通过warrior数据获取army_data
    '''
    temp_list = []
    data_list = []
    data = []
    data = warriorDataToInts(warriors)
    data2 = techDataToInts(teches["wall"].values()+ teches["hero"].values())
    #print "data :", data
    #print "data2 :", data2
    data_list = toInts(data)
    data2_list = toInts(data2)
    temp_list.append(data_list)
    #前端逻辑结尾用，具体数据没有意义
    temp_list.append(data2_list)
    #print "temp_list :", temp_list
    army_data = toInts(temp_list)
    #print "army_data:", army_data

    return army_data

def get_building_warrior_data(player):
    new_warrior_dict_list = []
    playbuildings = player.buildings.all()

    for playerbuilding in playbuildings.values():
        warrior_dict = {}
        # 防御塔的升级不是建筑升级，等级在player.wallWarriorIds
        warriorlevel = get_warriorlevel(playerbuilding.building.buildingToWarriorId, playerbuilding.level)
        #　相当于在要塞上附加的建筑信息，这个专门就是做城门的建筑的.
        if playerbuilding.building.is_castle:
            warriorlevel_wall = get_warriorlevel(playerbuilding.building.buildingToWarriorId - 800000, 1)
            if warriorlevel_wall:
                warrior_dict["nodeId"] = 0
                warrior_dict["level"] = warriorlevel_wall.level
                warrior_dict["upgrade"] = 0
                warrior_dict["star"] = 0
                warrior_dict["leftGrid"] = playerbuilding.centerX
                warrior_dict["topGrid"] = playerbuilding.centerY
                warrior_dict["serverEnergy"] = 0
                warrior_dict["gid"] = warriorlevel_wall.warrior_id
                warrior_dict["serverHp"] = warriorlevel.hp
                warrior_dict["destinyLevel"] = 0
                warrior_dict["fireBuff"] = 10201
                warrior_dict["techIndex"] = ""
                new_warrior_dict_list.append(warrior_dict)
                warrior_dict = {}

        if warriorlevel:
            warrior_dict["nodeId"] = 0
            warrior_dict["level"] = warriorlevel.level
            warrior_dict["upgrade"] = 0
            warrior_dict["star"] = 0
            warrior_dict["leftGrid"] = playerbuilding.centerX
            warrior_dict["topGrid"] = playerbuilding.centerY
            warrior_dict["serverEnergy"] = 0
            warrior_dict["gid"] = warriorlevel.warrior_id
            warrior_dict["serverHp"] = warriorlevel.hp
            warrior_dict["destinyLevel"] = 0
            warrior_dict["fireBuff"] = 10201
            warrior_dict["techIndex"] = ""
            new_warrior_dict_list.append(warrior_dict)
    return new_warrior_dict_list

def get_robot_soldier_warrior_data(player):
    '''
    机器人城墙士兵数据
    '''
    new_warrior_dict_list = []
    from module.robot.api import get_robot
    robot = get_robot(player.id)
    defenseSiegeSoldierIds = [-1 for i in range(0, 5)]
    soldierLevel = [-1 for i in range(0, 5)]
    
    # 从1，2，3开排，再排0，4
    for i in range(1, 4):
        defenseSiegeSoldierIds[i] = len(robot.siegeSoldierIds) >= i and robot.siegeSoldierIds[i-1] or -1
        soldierLevel[i] = len(robot.siegeSoldierLevels) >= i and robot.siegeSoldierLevels[i-1] or -1

    defenseSiegeSoldierIds[0] = len(robot.siegeSoldierIds) >= 4 and robot.siegeSoldierIds[3] or -1
    soldierLevel[0] = len(robot.siegeSoldierLevels) >= 4 and robot.siegeSoldierLevels[3] or -1
    defenseSiegeSoldierIds[4] = len(robot.siegeSoldierIds) >= 5 and robot.siegeSoldierIds[4] or -1
    soldierLevel[4] = len(robot.siegeSoldierLevels) >= 5 and robot.siegeSoldierLevels[4] or -1
    for _i,soldierId in enumerate(defenseSiegeSoldierIds):
        if soldierId <= 0:
            #-1,未解锁 0,未投放士兵
            continue
        warrior_dict = {}
        warrior_dict["nodeId"] = 0
        warrior_dict["level"] = soldierLevel[_i]
        warrior_dict["upgrade"] = 0
        warrior_dict["star"] = 0
        warrior_dict["leftGrid"] = _i
        warrior_dict["topGrid"] = 0
        warrior_dict["serverEnergy"] = 0
        warrior_dict["gid"] = soldierId
        warrior_dict["serverHp"] = 1 # 生命值
        warrior_dict["destinyLevel"] = 0
        warrior_dict["fireBuff"] = 0
        warrior_dict["techIndex"] = ""
        new_warrior_dict_list.append(warrior_dict)
    return new_warrior_dict_list   

def get_soldier_warrior_data(player):
    '''
    城墙士兵数据
    '''
    if player.id < 0:
        #机器人
        return get_robot_soldier_warrior_data(player)

    new_warrior_dict_list = []
    for _i,soldierId in enumerate(player.defenseSiegeSoldierIds):
        if soldierId <= 0:
            #-1,未解锁 0,未投放士兵
            continue
        warrior_dict = {}
        for warrior in player.wallWarriorIds:
            if soldierId != warrior["soldierId"]:
                continue
            warrior_dict["nodeId"] = 0
            warrior_dict["level"] = warrior["soldierLevel"]
            warrior_dict["upgrade"] = 0
            warrior_dict["star"] = 0
            warrior_dict["leftGrid"] = _i
            warrior_dict["topGrid"] = 0
            warrior_dict["serverEnergy"] = 0
            warrior_dict["gid"] = soldierId
            warrior_dict["serverHp"] = 1 # 生命值
            warrior_dict["destinyLevel"] = 0
            warrior_dict["fireBuff"] = 0
            warrior_dict["techIndex"] = ""
            new_warrior_dict_list.append(warrior_dict)
    return new_warrior_dict_list        

def get_robot_tower_soldier_data(player):
    new_warrior_dict_list = []
    from module.robot.api import get_robot
    robot = get_robot(player.id)
    warriorlevel = get_warriorlevel(Static.HERO_WALL_SOLDIER_IDS[3]*100, robot.towerLevel)
    for i in range(2):
        warrior_dict = {}
        warrior_dict["nodeId"] = 0
        warrior_dict["level"] = warriorlevel.level
        warrior_dict["upgrade"] = 0
        warrior_dict["star"] = 0
        warrior_dict["leftGrid"] = i # X
        warrior_dict["topGrid"] = 0 # Y
        warrior_dict["serverEnergy"] = 0
        warrior_dict["gid"] = warriorlevel.warrior_id
        warrior_dict["serverHp"] = warriorlevel.hp # 生命值
        warrior_dict["destinyLevel"] = 0
        warrior_dict["fireBuff"] = 10201
        warrior_dict["techIndex"] = ""
        new_warrior_dict_list.append(warrior_dict)
    return new_warrior_dict_list    


def get_tower_soldier_data(player):
    """
        获取攻城战防御塔士兵数据
    """
    if player.id < 0:
        # 机器人
        return get_robot_tower_soldier_data(player)
    new_warrior_dict_list = []
    for warrior in player.wallWarriorIds:
        if warrior["soldierId"] != Static.HERO_WALL_SOLDIER_IDS[3]: # 防御塔的士兵ID
            continue
        warriorlevel = get_warriorlevel(warrior["soldierId"]*100, warrior["soldierLevel"])
        for i in range(2):
            warrior_dict = {}
            warrior_dict["nodeId"] = 0
            warrior_dict["level"] = warriorlevel.level
            warrior_dict["upgrade"] = 0
            warrior_dict["star"] = 0
            warrior_dict["leftGrid"] = i # X
            warrior_dict["topGrid"] = 0 # Y
            warrior_dict["serverEnergy"] = 0
            warrior_dict["gid"] = warriorlevel.warrior_id
            warrior_dict["serverHp"] = warriorlevel.hp # 生命值
            warrior_dict["destinyLevel"] = 0
            warrior_dict["fireBuff"] = 10201
            warrior_dict["techIndex"] = ""
            new_warrior_dict_list.append(warrior_dict)
        break
    return new_warrior_dict_list    


def get_warrior_data(player, teches, defenseLayout):
    '''
    更新最新的warrior数据
    '''
    if player.id < 0:
        #机器人情况(机器人只有五个英雄，不确定哪个)
        from module.robot.api import get_robot
        robot = get_robot(player.id)
        heroIds = robot.heroes
        defenseList = []
        default_poses = Static.HERO_DEFENCE_POS
        i = 0
        for defenseheroid in heroIds[0:5]:
            defenseList.append(defenseheroid)
            defenseList.append(default_poses[i])
            i += 1
        defenseLayout = defenseList
    new_warrior_dict_list = []
    #haveWall = False # 没用上
    defenseHeroLen = len(defenseLayout)/2

    for i in range(0, defenseHeroLen):
        warrior_dict = {}
        playerhero_id, pos = defenseLayout[i*2:(i+1)*2]
        playerhero = player.heroes.get(playerhero_id)
        if playerhero:
            playerheroteam = player.heroteams.get(playerhero.warrior.hero.heroTeamId)
            warrior_dict["nodeId"] = pos
            warrior_dict["level"] = playerhero.level
            warrior_dict["upgrade"] = playerhero.upgrade
            warrior_dict["star"] = playerhero.star
            warrior_dict["destinyLevel"] = playerhero.destinyLevel
            warrior_dict["fireBuff"] = 0#player.fireBuff
            all_hero_artifacts = get_playerhero_artifacts(player, playerhero)
            warrior_dict["artifactInfo"] = []
            for artifact in all_hero_artifacts:
                warrior_dict["artifactInfo"].append(artifact.artifact_id)
                warrior_dict["artifactInfo"].append(artifact.level)
                warrior_dict["artifactInfo"].append(artifact.refineLevel)

            player_hero_equips = get_playerhero_equips(player, playerhero)
            warrior_dict["equipsInfo"] = []
            for playerequip in player_hero_equips:
                warrior_dict["equipsInfo"].append(playerequip.equip_id)
                warrior_dict["equipsInfo"].append(playerequip.level)
                warrior_dict["equipsInfo"].append(playerequip.refineLevel)

            warrior_dict["spellsInfo"] = []
            skill_id = 0
            skill_level = 0
            for i in range(1,5):
                skill_id, skill_level = playerhero.get_skill_info(i)
                if skill_id:
                    warrior_dict["spellsInfo"].append(skill_id)
                    warrior_dict["spellsInfo"].append(skill_level)

            warrior_dict["teamInfo"] = []
            warrior_dict["teamInfo"].append(playerheroteam.teamId)
            warrior_dict["teamInfo"].append(playerheroteam.level)

            warrior_dict["masterInfo"] = []
            warrior_dict["masterInfo"].append(playerhero.equipEnhanceMasterId)
            warrior_dict["masterInfo"].append(playerhero.equipRefineMasterId)
            warrior_dict["masterInfo"].append(playerhero.artifactEnhanceMasterId)
            warrior_dict["masterInfo"].append(playerhero.artifactRefineMasterId)
            warrior_dict["leftGrid"] = 0
            warrior_dict["serverEnergy"] = 0
            warrior_dict["topGrid"] = 0
            warrior_dict["gid"] = playerhero.cardId
            warrior_dict["techIndex"] = range(1, len(teches["hero"])+1)
            hero = playerhero.warrior.hero
            herostar = get_herostar(hero.cardId, playerhero.star)
            warrior_dict["serverHp"] = hero.hp + herostar.hpGrow * (playerhero.level - 1)
            new_warrior_dict_list.append(warrior_dict)
    return new_warrior_dict_list

def get_tech_data(player):
    '''
    获取科技数据
    '''
    #print "跟新前 建筑科技结构为：", tech_dict_list
    tech_dicts = {"wall":{
            39: {
                    "target":1,
                    "value": 0,
                    "abilityType": 39,
                }     
        },
        "hero":{}
    }
    # all_player_buildings = player.buildings.all()
    # for building_id, player_building in all_player_buildings.items():
    #     building = player_building.building
        #if building.is_deco:
        #    deco_building = BuildingDecoBattle.get_buildingdecobattle_by_building_and_level(building, player_building.level)
        #     if deco_building:
        #
        #         ability_id_list = deco_building.abilities
        #         ability_val_list = deco_building.abilityValues
        #         for i in range(0, len(ability_id_list)):
        #             abilityType = ability_id_list[i]
        #             if abilityType == 39:
        #                 tech_dicts["wall"][abilityType]["value"] += ability_val_list[i]
        #             else:
        #                 if abilityType not in tech_dicts["hero"]:
        #                     tech_dicts["hero"][abilityType] = {}
        #                     tech_dicts["hero"][abilityType]["target"] = 0
        #                     tech_dicts["hero"][abilityType]["abilityType"] = abilityType
        #                     tech_dicts["hero"][abilityType]["value"] = ability_val_list[i]
        #                 else:
        #                     tech_dicts["hero"][abilityType]["value"] += ability_val_list[i]

    return tech_dicts

def get_army_data(player):
    '''
    竞技场的防守阵容
    army_data数据
    更新player 的 army_data 数据
    '''
    teches = get_tech_data(player)
    warriors = get_warrior_data(player, teches, player.defenseHeroLayout)
    army_data = get_army_data_by_warrior_dict_list(warriors, teches)

    return army_data

def get_building_army_data(player):
    '''
    攻城战的防守阵容
    '''
    teches = get_tech_data(player)
    building_warriors = get_building_warrior_data(player) + get_warrior_data(player, teches, player.defenseSiegeLayout) + get_soldier_warrior_data(player) + get_tower_soldier_data(player)
    building_army_data = get_army_data_by_warrior_dict_list(building_warriors, teches)
    return building_army_data


