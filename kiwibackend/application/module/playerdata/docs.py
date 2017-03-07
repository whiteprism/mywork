# -*- coding: utf-8 -*-
import datetime
from common.decorators.memoized_property import memoized_property
import cPickle
from submodule.fanyoy.redis import PlayerDynamicRedisHandler
from module.playerhero.docs import PlayerHero, PlayerArmy, PlayerHeroTeam, PlayerRampartSoldiers
from module.playeritem.docs import PlayerItem, PlayerStoreRecord, PlayerTowerStoreRecord
from module.playerbuilding.docs import PlayerBuilding, PlayerBuildingFragment
from module.playerequip.docs import PlayerEquip, PlayerEquipFragment
from module.playerartifact.docs import PlayerArtifact, PlayerArtifactFragment
from module.playergashapon.docs import PlayerGashapon
from module.playersoul.docs import PlayerSoul
from module.playerarena.docs import PlayerArenaShop
from module.playermysteryshop.docs import PlayerMysteryShop
from module.guild.docs import PlayerGuildShop, PlayerGuild
from module.playerPVP.docs import PlayerPVP, PlayerSiegeBattle
from module.playeryuanbo.docs import PlayerYuanboShop
from module.playerinstance.docs import PlayerInstanceLevel, PlayerEliteInstanceLevel, PlayerRaidInstance, PlayerElementTower
from module.playeractivity.docs import PlayerActivity
from module.playerplant.docs import PlayerPlant

class SingleDataHandler(object):
    """
    操作
    """
    def __init__(self, player):
        self._playerdata = None
        self._value = None
        self._param = None
        self.player = player

    def init_data(self, playerdata, cls, datas_str, param):
        self._playerdata = playerdata
        self._param = param

        if datas_str:
            data = cPickle.loads(datas_str)
            self._value = cls.from_json(data)
            self._value.data_handler = self
            self._value.load(self.player)
        else:
            self._value = cls()
            self._value.data_handler = self
            self._value.new(self.player)
            self._value.load(self.player)
        

    def get(self):
        return self._value

    def update(self):
        self._value.updated_at = datetime.datetime.now()
        self._playerdata.add_save_param(self._param)


    @property
    def bin_data(self):
        return cPickle.dumps(self._value.to_json())

class DataHandler(object):
    """
    操作
    """
    def __init__(self, player):
        self._pk = 0
        self._value_dicts = {}
        self._value_objs = {}
        self._param = ""
        self._playerdata = None
        #self.handle_logs = {} # 1添加 2修改 3删除
        self._cls = None #对应的class
        self.player = player

    def __len__(self):
        return len(self._value_dicts)

    def init_data(self, playerdata, cls, datas_str, param):
        self._cls = cls
        if datas_str:
            datas = cPickle.loads(datas_str)
            self._pk = datas["pk"]
            self._value_dicts = datas["values"]

        self._playerdata = playerdata
        self._param = param

    def all(self):
        _keys = set(self._value_dicts.keys()) - set(self._value_objs.keys())
        for _key in _keys:
            obj = self._cls.from_json(self._value_dicts[_key])
            obj.load(self.player)
            self._value_objs[_key] = obj
        return self._value_objs
    
    def get(self, pk):
        if not self._value_objs.has_key(pk) and self._value_dicts.has_key(pk):
            obj = self._cls.from_json(self._value_dicts[pk])
            obj.load(self.player)
            self._value_objs[pk] = obj
        return self._value_objs.get(pk, None)

    def create(self, **argvs):
        obj = self._cls(**argvs)
        if not obj.pk:
            self._pk += 1
            obj.pk = self._pk
        obj.new(self.player)
        obj.load(self.player)
        self._value_objs[obj.pk] = obj
        return obj

    def get_or_create(self, pk, **argvs):
        is_new = False
        obj = self.get(pk)

        if not obj:
            is_new = True
            if pk:
                argvs["pk"] = pk
            obj = self.create(**argvs)
        return is_new, obj

    def get_count_by_key(self, key, value):
        count = 0
        for _pk, _value_dict in self._value_dicts.items():
            obj = self.get(_pk)
            if obj and getattr(obj, key) == value:
                count += 1
        return count

    def get_list_by_key(self, key, value):
        datas = []
        for _pk, _value_dict in self._value_dicts.items():
            data = self.get(_pk)
            if getattr(data, key) == value:
                datas.append(data)
            
        return datas

    def get_by_pks(self, pks):
        data = {}
        for pk in pks:
            obj = self.get(int(pk))
            if obj:
                data[obj.pk] = obj
        return data

    def add(self, obj):
        if isinstance(obj, self._cls):
            obj.updated_at = datetime.datetime.now()
            self._value_objs[obj.pk] = obj
            self._value_dicts[obj.pk] = obj.to_json()
            self._playerdata.add_save_param(self._param)

    def delete(self, pk):
        del self._value_objs[pk]
        if pk in self._value_dicts:
            del self._value_dicts[pk]
        self._playerdata.add_save_param(self._param)

    def update(self, obj):
        if isinstance(obj, self._cls):
            self._playerdata.add_save_param(self._param)
            obj.updated_at = datetime.datetime.now()
            self._value_dicts[obj.pk] = obj.to_json()

    @property
    def bin_data(self):
        datas = {"pk":self._pk, "values": self._value_dicts}
        return cPickle.dumps(datas)

class PlayerData(PlayerDynamicRedisHandler):
    all_params = {
        "activities_bin" : {
            'default': "",  'type': str,
        }, 
        "heroes_bin" : {
            'default': "",  'type': str,
        }, 
        "armies_bin" : {
            'default': "",  'type': str,
        }, 
        "souls_bin" : {
            'default': "",  'type': str,
        }, 
        "items_bin" : {
            'default': "",  'type': str,
        }, 
        "buyrecords_bin" : {
            'default': "",  'type': str,
        },
        "buytowerrecords_bin" : {
            'default': "",  'type': str,
        },
        "buildings_bin" : {
            'default': "",  'type': str,
        }, 
        "buildingplants_bin" : {
            'default': "",  'type': str,
        }, 
        "equips_bin" : {
            'default': "",  'type': str,
        }, 
        "instancelevels_bin" : {
            'default': "",  'type': str,
        }, 
        "eliteinstancelevels_bin" : {
            'default': "",  'type': str,
        }, 
        "raidinstances_bin" : {
            'default': "",  'type': str,
        }, 
        "elementTower_bin" : {
            'default': "",  'type': str,
        }, 
        "equipfragments_bin" : {
            'default': "",  'type': str,
        }, 
        "artifacts_bin" : {
            'default': "",  'type': str,
        }, 
        "artifactfragments_bin" : {
            'default': "",  'type': str,
        },
        "buildingfragments_bin" : {
            'default': "",  'type': str,
        },
        "gashapons_bin" : {
            'default': "",  'type': str,
        }, 

        "arenashop_bin" : {
            'default': "",  'type': str,
        },
        "guildshop_bin" : {
            'default': "",  'type': str,
        },
        "guild_bin" : {
            'default': "",  'type': str,
        },
        "mysteryshop_bin" : {
            'default': "",  'type': str,
        }, 
        "yuanboshop_bin" : {
            'default': "",  'type': str,
        }, 
        "PVP_bin" : {
            'default': "",  'type': str,
        },
        "SiegeBattle_bin" : {
            'default': "",  'type': str,
        },
        "heroteams_bin" : {
            'default': "",  'type': str,
        },
        "rampartSoldiers_bin" : {
            'default': "",  'type': str,
        },
    }
    player = None


    def __init__(self, *argv, **argvs):
        super(PlayerData, self).__init__(*argv, **argvs)
        self._save_params = []

    def add_save_param(self, param):
        if param not in self._save_params:
            self._save_params.append(param)

    def _datahandler(self, cls, key):
        handler = DataHandler(self.player)
        handler.init_data(self, cls, getattr(self, "%s_bin" % key), key)
        return handler

    def _singledatahandler(self, cls, key):
        handler = SingleDataHandler(self.player)
        handler.init_data(self, cls, getattr(self, "%s_bin" % key), key)
        return handler.get()

    @memoized_property
    def activities(self):
        return self._datahandler(PlayerActivity, "activities")

    @memoized_property
    def heroes(self):
        return self._datahandler(PlayerHero, "heroes")

    @memoized_property
    def heroteams(self):
        return self._datahandler(PlayerHeroTeam, "heroteams")

    @memoized_property
    def armies(self):
        return self._singledatahandler(PlayerArmy, "armies")
        
    @memoized_property
    def souls(self):
        return self._datahandler(PlayerSoul, "souls")

    @memoized_property
    def items(self):
        return self._datahandler(PlayerItem, "items")

    @memoized_property
    def buyrecords(self):
        return self._datahandler(PlayerStoreRecord, "buyrecords")


    @memoized_property
    def buytowerrecords(self):
        return self._datahandler(PlayerTowerStoreRecord, "buytowerrecords")

    @memoized_property
    def buildings(self):
        return self._datahandler(PlayerBuilding, "buildings")

    @memoized_property
    def buildingplants(self):
        return self._datahandler(PlayerPlant, "buildingplants")

    @memoized_property
    def rampartSoldiers(self):
        return self._datahandler(PlayerRampartSoldiers, "rampartSoldiers")

    @memoized_property
    def equips(self):
        return self._datahandler(PlayerEquip, "equips")

    @memoized_property
    def instancelevels(self):
        return self._datahandler(PlayerInstanceLevel, "instancelevels")

    @memoized_property
    def eliteinstancelevels(self):
        return self._datahandler(PlayerEliteInstanceLevel, "eliteinstancelevels")

    @memoized_property
    def raidinstances(self):
        return self._datahandler(PlayerRaidInstance, "raidinstances")

    @memoized_property
    def elementTower(self):
        return self._singledatahandler(PlayerElementTower, "elementTower")

    @memoized_property
    def equipfragments(self):
        return self._datahandler(PlayerEquipFragment, "equipfragments")

    @memoized_property
    def artifactfragments(self):
        return self._datahandler(PlayerArtifactFragment, "artifactfragments")
        
    @memoized_property
    def buildingfragments(self):
        return self._datahandler(PlayerBuildingFragment, "buildingfragments")

    @memoized_property
    def artifacts(self):
        return self._datahandler(PlayerArtifact, "artifacts")

    @memoized_property
    def gashapons(self):
        return self._datahandler(PlayerGashapon, "gashapons")

    @memoized_property
    def arenashop(self):
        return self._singledatahandler(PlayerArenaShop, "arenashop")

    @memoized_property
    def mysteryshop(self):
        return self._singledatahandler(PlayerMysteryShop, "mysteryshop")

    @memoized_property
    def guildshop(self):
        return self._singledatahandler(PlayerGuildShop, "guildshop")

    @memoized_property
    def guild(self):
        return self._singledatahandler(PlayerGuild, "guild")

    @memoized_property
    def PVP(self):
        return self._singledatahandler(PlayerPVP, "PVP")

    @memoized_property
    def SiegeBattle(self):
        return self._singledatahandler(PlayerSiegeBattle, "SiegeBattle")

    @memoized_property
    def yuanboshop(self):
        return self._singledatahandler(PlayerYuanboShop, "yuanboshop")

    def prepare_save(self):
        for _param in self._save_params:
            self.set("%s_bin" % _param,  getattr(self, _param).bin_data)
        self.save()
