# -*- coding: utf-8 -*-
from mongoengine import *
from common.docs import PlayerRedisDataBase, PlayerRedisDataListBase
from common.decorators.memoized_property import memoized_property
from common.static import Static
# from module.utils import delta_time
import time
from submodule.fanyoy.redis.increment import _IncrementId_instance
from module.playerbuilding.docs import PlayerBuilding
from module.building.api import get_buildingplant, get_building

class PlantStatusType():
    SEDDLING = 0 #幼苗期
    GROWTH = 1 #成长期
    MATURATION = 2 #成熟期
    WITHERED = 3 #枯萎期

class PlayerPlant(PlayerRedisDataBase):
    """
    玩家植物
    """
    centerX = FloatField()
    centerY = FloatField()
    plantId = IntField(default=0)
    buildingId = IntField(default=0)
    status = IntField(default=0)
    harvestTimes = IntField(default=0)
    # endDatetime = DateTimeField(default=datetime.datetime.now) 
    # startDatetime = DateTimeField(default=datetime.datetime.now)
    timeLeft = IntField(default=0) # unix时间点

    @classmethod
    def _incrment_id(cls):
        """
        获取自增id
        """
        return _IncrementId_instance.incr(PlayerBuilding.__name__)

    @memoized_property
    def plant(self):
        return get_buildingplant(self.plantId)

    @memoized_property
    def building(self):
        return get_building(self.buildingId)

    @property
    def harvestLeftTimes(self):
        return self.plant.harvestTimes - self.harvestTimes

    @property
    def is_seedling(self):
        return self.status == PlantStatusType.SEDDLING

    @property
    def is_growth(self):
        return self.status == PlantStatusType.GROWTH

    @property
    def is_maturation(self):
        return self.status == PlantStatusType.MATURATION

    @property
    def is_withered(self):
        return self.status == PlantStatusType.WITHERED

    def set_seedling(self):
        self.status = PlantStatusType.SEDDLING

    def set_growth(self):
        self.status = PlantStatusType.GROWTH

    def set_maturation(self):
        self.status = PlantStatusType.MATURATION

    def set_withered(self):
        self.status = PlantStatusType.WITHERED

    @property
    def costs(self):
        return self.plant.costs()

    def harvest(self):
        """
        采摘
        """
        self.harvestTimes += 1
        # self.startDatetime = datetime.datetime.now()
        if self.harvestLeftTimes > 0:
            #还可以再采摘
            self.set_growth()
            self.timeLeft = time.time() + self.plant.harvestInterval
            # self.endDatetime = self.startDatetime + datetime.timedelta(seconds=self.plant.harvestInterval)
        else:
            self.set_withered()
            self.timeLeft = 0
        return self.plant.rewards

    def cultivate(self):
        """
        种植
        """
        self.set_seedling()
        self.timeLeft = time.time() + self.plant.growthInterval
        # self.startDatetime = datetime.datetime.now()
        # self.endDatetime = self.startDatetime + datetime.timedelta(seconds=self.plant.growthInterval)

    @property
    def can_change_status(self):
        if self.is_maturation or self.is_withered:
            return False
        return True

    def check_status(self):
        # now = datetime.datetime.now()
        status_change = False

        if self.is_seedling:
            #幼苗期
            overtime = time.time() - self.timeLeft
            if overtime > 0:
                #进入成长期
                self.set_growth()
                self.timeLeft = self.timeLeft + self.plant.matureInterval
                status_change = True
        if self.is_growth:
            #成长期
            overtime = time.time() - self.timeLeft
            if overtime > 0:
                #进入成熟期
                self.set_maturation()
                self.timeLeft = -1
                status_change = True
        if status_change == True:
            self.player.update_buildingplant(self, True)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["harvestTimes"] = self.harvestLeftTimes
        return dicts