#-*- encoding:utf-8 -*-
from instance.models import Instance, InstanceLevel, EliteInstanceLevel, Enemy, Raid, RaidLevelConf, InstanceReward, TriggerData, Trigger, Zone, TriggerInfo, GuildInstanceLevel, SmallGame, SmallGameReward, ElementTowerInstance, ElementTowerLevel, ElementTowerBuff

def update_instance_cache():
    Instance.create_cache()
    InstanceLevel.create_cache()
    EliteInstanceLevel.create_cache()
    Raid.create_cache()
    RaidLevelConf.create_cache()
    InstanceReward.create_cache()
    Enemy.create_cache()
    Trigger.create_cache()
    TriggerInfo.create_cache()
    TriggerData.create_cache()
    Zone.create_cache()
    GuildInstanceLevel.create_cache()
    SmallGame.create_cache()
    SmallGameReward.create_cache()
    ElementTowerInstance.create_cache()
    ElementTowerLevel.create_cache()
    ElementTowerBuff.create_cache()

def get_all_guildinstancelevels():
    '''
    获取所有关卡
    '''
    guildInstanceLevels = GuildInstanceLevel.get_all_list()
    return sorted(guildInstanceLevels, key=lambda x: x.id)

# TODO 函数重复 下面有
def get_guildinstancelevel(id):
    return GuildInstanceLevel.get(int(id))

def get_raidenemytoreward(pk):
    return RaidEnemyToReward.get(int(pk))


def get_raidinstances():
    '''
    获取所有活动副本
    '''
    return Raid.get_all_list()

def get_raidinstance(raid_id):
    '''
    获取活动副本
    '''
    return Raid.get(raid_id)

def get_raidlevel(level_id):
    '''
    获取活动副本
    '''
    return RaidLevelConf.get(level_id)

def get_raidlevels():
    '''
    获取活动副本
    '''
    return RaidLevelConf.get_all_list()

def get_instances():
    '''
    获取所有章节
    '''
    instances = Instance.get_all_list()
    return sorted(instances, key=lambda x: x.id)

def get_instance(instance_id):
    """
    获取章节信息
    """
    return Instance.get(int(instance_id))

def get_all_instancelevels():
    '''
    获取所有关卡
    '''
    instanceLevels = InstanceLevel.get_all_list()
    return sorted(instanceLevels, key=lambda x: x.id)

def get_all_eliteinstancelevels():
    '''
    获取所有精英关卡
    '''
    eliteInstanceLevels = EliteInstanceLevel.get_all_list()
    return sorted(eliteInstanceLevels, key=lambda x: x.id)


def get_instancelevels_by_instance_id(instance_id):
    """
    获取对应章节的levels
    """
    return InstanceLevel.get_instancelevel_by_instance_id(instance_id)


def get_eliteinstancelevel_by_instance_id(instance_id):
    """
    获取对应章节的levels
    """
    return EliteInstanceLevel.get_eliteinstancelevel_by_instance_id(instance_id)
    
def get_instancelevel(level_id):
    '''
    获取对应id关卡
    '''
    return InstanceLevel.get(level_id)

def get_eliteinstancelevel(level_id):
    '''
    获取对应id关卡
    '''
    return EliteInstanceLevel.get(level_id)

def get_elite_data(instanceDict):
    '''
    转换精英副本数据
    '''
    if instanceDict.has_key("eliteInstanceReward"):
        instanceDict["reward"] = instanceDict["eliteInstanceReward"]
        del instanceDict["eliteInstanceReward"]
    if instanceDict.has_key("InstanceReward"):
        del instanceDict["InstanceReward"]
    if instanceDict.has_key("elitePowerCost"):
        instanceDict["powerCost"] = instanceDict["elitePowerCost"]
        del instanceDict["elitePowerCost"]
    if instanceDict.has_key("elitePlayerExp"):
        instanceDict["playerExp"] = instanceDict["elitePlayerExp"]
        del instanceDict["elitePlayerExp"]

    if instanceDict.has_key("minUserLevel"):
        del instanceDict["minUserLevel"]
    if instanceDict.has_key("heroExp_int"):
        del instanceDict["heroExp_int"]
    if instanceDict.has_key("golds_int"):
        del instanceDict["golds_int"]
    if instanceDict.has_key("revisionScale_float"):
        del instanceDict["revisionScale_float"]

    if instanceDict.has_key("eliteHeroIds"):
        instanceDict["heroGids"] = instanceDict["eliteHeroIds"]
        del instanceDict["eliteHeroIds"]
    if instanceDict.has_key("eliteHeroExp"):
        instanceDict["heroExp"] = instanceDict["eliteHeroExp"]
        del instanceDict["eliteHeroExp"]
    if instanceDict.has_key("eliteGold"):
        instanceDict["gold"] = instanceDict["eliteGold"]
        del instanceDict["eliteGold"]
    if instanceDict.has_key("eliteRevisionScale"):
        instanceDict["revisionScale"] = instanceDict["eliteRevisionScale"]
        del instanceDict["eliteRevisionScale"]
    
    return instanceDict

def get_level_data(instanceDict):
    '''
    转换普通副本数据
    '''
    if instanceDict.has_key("InstanceReward"):
        instanceDict["reward"] = instanceDict["InstanceReward"]
        del instanceDict["InstanceReward"]
    if instanceDict.has_key("eliteInstanceReward_int"):
        del instanceDict["eliteInstanceReward_int"]
    if instanceDict.has_key("eliteGold"):
        del instanceDict["eliteGold"]
    if instanceDict.has_key("eliteHeroExp"):
        del instanceDict["eliteHeroExp"]
    if instanceDict.has_key("eliteRevisionScale"):
        del instanceDict["eliteRevisionScale"]
    if instanceDict.has_key("eliteConstrainData_int"):
        del instanceDict["eliteConstrainData_int"]
    if instanceDict.has_key("eliteMinUserLevel"):
        del instanceDict["eliteMinUserLevel"]
    if instanceDict.has_key("eliteWallHp"):
        del instanceDict["eliteWallHp"]
    if instanceDict.has_key("elitePowerCost"):
        del instanceDict["elitePowerCost"]
    if instanceDict.has_key("eliteHeroIds"):
        del instanceDict["eliteHeroIds"]

    return instanceDict

def get_zones():
    return Zone.get_all_list()

def get_triggers():
    return Trigger.get_all_list()

def get_triggerinfo(pk):
    return TriggerInfo.get(int(pk))

def get_guildinstanceLevel(pk):
    return GuildInstanceLevel.get(int(pk))

def get_guildinstanceLevels():
    return GuildInstanceLevel.get_all_list()

def get_smallGames():
    return SmallGame.get_all_list()

def get_elementtowerinstances():
    return ElementTowerInstance.get_all_list()

def get_elementtowerinstance(pk):
    return ElementTowerInstance.get(int(pk))

def get_elementtowerbuffs():
    return ElementTowerBuff.get_all_list()

def get_elementtowerbuff(pk):
    return ElementTowerBuff.get(int(pk))
