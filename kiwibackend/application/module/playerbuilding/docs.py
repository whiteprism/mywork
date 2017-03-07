# -*- coding: utf-8 -*-
from mongoengine import *
from common.docs import PlayerDataBase, PlayerRedisDataBase, PlayerRedisDataListBase
from common.decorators.memoized_property import memoized_property
from common.static import Static
from module.utils import delta_time
import datetime
from module.building.api import get_building, get_buildingfragment, get_buildingattribute
from submodule.fanyoy.redis.increment import _IncrementId_instance
from module.common.actionlog import ActionLogWriter
import math
import random

class BuildingStatusType():
    NORMAL = 0 #正常状态
    BUILDING = 1 #建造状态
    PRODUCING = 2 #生产状态
    UPGRADING = 4 #升级状态
    UPGRADED = 5 #

class PlayerBuilding(PlayerRedisDataBase):
    """
    玩家建筑
    """
    centerX = FloatField()
    centerY = FloatField()
    level = IntField(default=1)  
    productions_dict = DictField(default={})
    status = IntField(default=0)  
    building_id = IntField(default=0)
    end_datetime = DateTimeField(default=datetime.datetime.now) 
    start_datetime = DateTimeField(default=datetime.datetime.now)
    attrList = DictField(default={})
    # soldierId = IntField(default=0) # 配置点存储士兵

    @classmethod
    def _incrment_id(cls):
        """
        获取自增id
        """
        return _IncrementId_instance.incr(cls.__name__)

    @memoized_property
    def building(self):
        return get_building(self.building_id)

    @property
    def population(self):
        #_populations = self.building.population_confs

        #for _p in _populations:
        #    if _p.level == self.level:
        #        return _p.popCount
        return 0 

    @property
    def produce_soldier_amount(self):

        if self.building.is_hordebarrack:
            return Static.BUILDING_HORDEBARRACK_PRODUCE_SOLDIER_RATIO * self.level
        else:
            return 0

    @property
    def is_normal(self):
        return self.status == BuildingStatusType.NORMAL

    @property
    def is_building(self):
        return self.status == BuildingStatusType.BUILDING

    @property
    def is_producing(self):
        return self.status == BuildingStatusType.PRODUCING

    @property
    def is_upgrading(self):
        return self.status == BuildingStatusType.UPGRADING

    @property
    def timeLeft(self):
        over_time = 0
        if self.is_normal :
            if self.building.is_goldmine or  self.building.is_loggingfield:
                  over_time = delta_time(self.start_datetime)
        else:
            over_time = delta_time(datetime.datetime.now(), self.end_datetime)

        return over_time if over_time > 0 else 0

    def goldmine_harvest(self):
        """
        金矿采集
        """
        self.start_datetime = datetime.datetime.now() #重新计时
       # self.end_datetime = self.start_datetime

    def goldmine_compute(self):
        """
        金矿金币计算
        """
        storage = 0
        over_time = delta_time(self.start_datetime) 
        golden_level = self.building.golden_levels[self.level]
    
        _gold = 0

        _gold = int(math.ceil(over_time / 3600.0 * golden_level.productionPerHour))

        if _gold > golden_level.storage:
            _gold = golden_level.storage 

        return _gold
 
    def upgrade(self, upgrade_info):
        """
        升级
        """
        self.end_datetime = datetime.timedelta(seconds=upgrade_info.useTime) + datetime.datetime.now()
        self.status = BuildingStatusType.UPGRADING
        return True

    def check_upgrade(self):
        if self.is_upgrading:
            if self.upgrade_over():
                self.status = BuildingStatusType.UPGRADED
                return True
        else:
            return False

    def upgrade_over(self, speed=False):
        '''
        前端通知建筑物升级结束
        '''
        if self.timeLeft <= 1 or speed: #合理误差1s
            self.status = BuildingStatusType.NORMAL
            self.start_datetime = datetime.datetime.now() #金矿重置
            self.end_datetime = self.start_datetime #金矿重置
            self.level += 1
            return True
        return False

    def produce_soldier_begin(self):
        self.start_datetime = datetime.datetime.now()
        self.end_datetime = self.start_datetime
        self.productions_dict = {}

    def produce_soldier(self, warrior_id, number, production, sort=1):
        warrior_id = str(warrior_id)
        self.productions_dict[warrior_id] = {"warrior_id":int(warrior_id),"number":number, "sort": sort, "cost":production.useTime, "type":production.productionType}
        self.end_datetime += datetime.timedelta(seconds=production.useTime*number)  

    def produce_soldier_end(self):
        self.status = BuildingStatusType.PRODUCING

    def producing_soldier(self, player, speed=False):
        _productions = self.productions_dict.values()
        _productions.sort(key=lambda x: x["sort"])
        now = datetime.datetime.now()

        is_over = True
        is_produce_soldier = False
        for _p in _productions:
            
            if not is_over:
                break

            warrior_id = str(_p["warrior_id"])
            for i in range(0, _p["number"]):
                if (self.start_datetime +  datetime.timedelta(seconds=_p["cost"]-1)).replace(tzinfo=None) <= now or speed:
                    if _p["type"] == 1:
                        # player.armies.acquire(warrior_id, 1)
                        # player.armies.drill_end(warrior_id, 1)
                        # player.dailytask_going(Static.DAILYTASK_CATEGORY_PRODUCE_SOLDIER, number=1, is_incr=True, is_series=True)
                        # player.task_going(Static.TASK_CATEGORY_SOLDIER_PRODUCT, number=1, is_incr=True, is_series=True)
                        pass
                    else:
                        player.levelup_hero_warriors(warrior_id)

                    self.start_datetime += datetime.timedelta(seconds=_p["cost"])
                    self.productions_dict[warrior_id]["number"] -= 1
                    is_produce_soldier = True
                else:
                    #正在生产
                    is_over = False
                    #跳出个数循环
                    break
        
        if is_over:
            self.status = BuildingStatusType.NORMAL
            self.productions_dict = {}
        return is_produce_soldier

    def random_attrbutes(self):
        #self.building.attrList 是 属性Id 的list
        attrs = self.building.attrList
        for pk in attrs:
            attr = get_buildingattribute(pk)
            value = random.uniform(attr.minValue, attr.maxValue)
            self.attrList[str(attr.attrType)] = float("%.4f" % value)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["buildingId"] = self.building_id
        dicts["timeLeft"] = self.timeLeft
        _productions = [{"production": int(k), "productionCount":v["number"], "productionType":v["type"],"sort": v["sort"]} for k,v in self.productions_dict.items()]
        _productions.sort(key=lambda x: x["sort"])
        dicts["productions"] = [{"production": v["production"], "productionCount":v["productionCount"], "productionType": v["productionType"]} for v in _productions]
        dicts["attrList"] = []
        attrs = self.attrList
        for attrType, extra in attrs.items():
            dicts["attrList"].append({
                "attrType": attrType,
                "extra": extra 
            })
        del dicts["building_id"]
        del dicts["end_datetime"]
        del dicts["start_datetime"]
        del dicts["productions_dict"]
        return dicts

class PlayerBuildingFragment(PlayerRedisDataListBase):
    """
    用户建筑碎片
    """
    #只在神像合成时使用
    @memoized_property
    def buildingfragment(self):
        return get_buildingfragment(self.buildingfragment_id)

    @property
    def buildingfragment_id(self):
        return self.obj_id
        
    def sub(self,delta_number=1, info=u""):
        """
        使用建筑碎片
        """
        before_number = self.count
        self.count -= delta_number
        if self.display:
            self.player.update_buildingfragment(self, True)
        else:
            self.player.delete_buildingfragment(self.buildingfragment_id, True)

        ActionLogWriter.buildingfragment_cost(self.player, self.buildingfragment, before_number, self.count, info)

    def add(self,delta_number=1, info=u""):
        before_number = self.count
        self.count += delta_number
        after_number = self.count

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["buildingFragmentId"] = self.obj_id
        del dicts["id"]
        return dicts
