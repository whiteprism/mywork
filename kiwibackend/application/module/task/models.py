# -*- coding: utf-8 -*-
from django.db import models
from common.models import CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler
from rewards.models import RewardsBase
from common.static import Static
from common.decorators.memoized_property import memoized_property

class TaskCondition(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"任务条件"
    c1 = models.IntegerField(u"condition1", default=0)
    count = models.IntegerField(u"目标数量", default=0)

    def __unicode__(self):
        return  u"任务条件：%s" % self.pk
        
    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        del dicts["id"]
        del dicts["c1"]
        return dicts

INIT_TASKS = {} #初始化任务
class Task(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"任务"
    name = models.CharField(u"name", max_length=200, default="")
    condition_id = models.IntegerField(u"任务条件ID", default=0)
    nameId = models.CharField(u"nameId", max_length=200, default=0)
    rewards_int = models.CharField(u"奖励ID,", max_length=200, default="")
    descriptionId = models.CharField(u"描述", max_length=200, default="")
    icon = models.CharField(u"icon", max_length=200, default="")
    link = models.IntegerField(u"link", default=0)
    nextTaskId = models.IntegerField(u"下个任务ID", default=0)
    level = models.IntegerField(u"开启等级", default=0)
    orderId = models.IntegerField(u"排序", default=0)
    category = models.IntegerField(u"类别", default=0)
    is_first = models.BooleanField(u"是否为初始任务", default=False)
    buildingId = models.IntegerField(u"入口建筑", default=0)

    def task_delegate(classname, base_types, dict):
        cls = type(classname, base_types, dict)
        try:
            cls.get_init_tasks()
        except:
            pass

        return cls

    __metaclass__ = task_delegate

    @classmethod
    def get_init_tasks(cls):
        if not INIT_TASKS:
            tasks = cls.get_all_list()
            for task in tasks:
                if task.is_first:
                    INIT_TASKS[task.category] = task.pk

        return INIT_TASKS

    @memoized_property
    def rewards(self):
        return [TaskReward.get(pk) for pk in self.rewards_int.strip().split(",") if pk]

    @memoized_property
    def condition(self):
        return TaskCondition.get(self.condition_id)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = self.pk
        if self.condition_id:
            dicts["condition"] = self.condition.to_dict()

        dicts["rewards"] = [_reward.to_dict() for _reward in self.rewards]

        del dicts["id"]
        del dicts["name"]
        del dicts["nextTaskId"]
        del dicts["is_first"]
        return dicts

INIT_DAILYTASKS = {} #初始化任务
class DailyTask(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"日常任务"
    name = models.CharField(u"name", max_length=200, default="")
    condition_id = models.IntegerField(u"condition id", default=0)
    nameId = models.CharField(u"nameId", max_length=200, default=0)
    rewards_int = models.CharField(u"奖励ID,", max_length=200, default="")
    descriptionId = models.CharField(u"描述", max_length=200, default="")
    icon = models.CharField(u"icon", max_length=200, default="")
    link = models.IntegerField(u"link", default=0)
    level = models.IntegerField(u"解锁等级", default=0)
    orderId = models.IntegerField(u"排序", default=0)
    category = models.IntegerField(u"类别", default=0)
    nextTaskId = models.IntegerField(u"下个任务ID", default=0)
    is_first = models.BooleanField(u"是否为初始任务", default=False)
    buildingId = models.IntegerField(u"入口建筑", default=0)
    activityGet = models.IntegerField(u"可以获取的活跃度", default=0)

    def __unicode__(self):
        return "DailyTask:%s" % self.name

    def task_delegate(classname, base_types, dict):
        cls = type(classname, base_types, dict)
        try:
            cls.get_init_dailytasks()
        except:
            pass
        return cls

    __metaclass__ = task_delegate

    @classmethod
    def get_init_dailytasks(cls):
        if not INIT_DAILYTASKS:
            tasks = cls.get_all_list()
            for task in tasks:
                if task.is_first:
                    INIT_DAILYTASKS[task.category] = task.pk
        return INIT_DAILYTASKS

    @memoized_property
    def rewards(self):
        return [TaskReward.get(int(float(pk))) for pk in self.rewards_int.strip().split(",") if pk]

    @property
    def is_vip_sweep(self):
        return self.category == Static.DAILYTASK_CATEGORY_VIP_SWEEP

    @property
    def is_welfare(self):
        return self.category == Static.DAILYTASK_CATEGORY_WELFARE

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = self.pk
        if self.condition_id:
            dicts["condition"] = self.condition.to_dict()
        dicts["rewards"] =  [_reward.to_dict() for _reward in self.rewards]

        del dicts["id"]
        del dicts["name"]
        del dicts["nextTaskId"]
        del dicts["is_first"]
        return dicts

    @memoized_property
    def condition(self):
        return TaskCondition.get(self.condition_id)

INIT_SEVEN_DAYS_TASKS = {} #七天乐初始化任务
class SevenDaysTask(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"七天乐任务"
    name = models.CharField(u"name", max_length=200, default="")
    condition_id = models.IntegerField(u"任务条件ID", default=0)
    nameId = models.CharField(u"nameId", max_length=200, default=0)
    rewards_int = models.CharField(u"奖励ID,", max_length=200, default="")
    descriptionId = models.CharField(u"描述", max_length=200, default="")
    icon = models.CharField(u"icon", max_length=200, default="")
    link = models.IntegerField(u"link", default=0)
    nextTaskId = models.IntegerField(u"下个任务ID", default=0)
    level = models.IntegerField(u"开启等级", default=0)
    orderId = models.IntegerField(u"排序", default=0)
    category = models.IntegerField(u"类别", default=0)
    is_first = models.BooleanField(u"是否为初始任务", default=False)
    buildingId = models.IntegerField(u"入口建筑", default=0)
    limitDay = models.IntegerField(u"时间限制", default=0)
    type = models.IntegerField(u"类型", default=0)
    pageId = models.IntegerField(u"页码", default=0)
    showId = models.IntegerField(u"统计", default=0)

    def task_delegate(classname, base_types, dict):
        cls = type(classname, base_types, dict)
        try:
            cls.get_init_seven_days_tasks()
        except:
            pass

        return cls

    __metaclass__ = task_delegate

    @classmethod
    def get_init_seven_days_tasks(cls):

        tasks = cls.get_all_list()
        for task in tasks:
            if task.is_first:
                INIT_SEVEN_DAYS_TASKS[task.category] = task.pk

        return INIT_SEVEN_DAYS_TASKS

    @memoized_property
    def rewards(self):
        return [TaskReward.get(pk) for pk in self.rewards_int.strip().split(",") if pk]

    @memoized_property
    def condition(self):
        return TaskCondition.get(self.condition_id)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = self.pk
        if self.condition_id:
            dicts["condition"] = self.condition.to_dict()

        dicts["rewards"] = [_reward.to_dict() for _reward in self.rewards]

        del dicts["id"]
        del dicts["name"]
        del dicts["nextTaskId"]
        del dicts["is_first"]
        return dicts



class DailyTaskActivity(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"日常任务活跃度"
    activityValue = models.IntegerField(u"任务条件ID", default=0)
    rewards_int = models.CharField(u"奖励ID,", max_length=200, default="")


    @memoized_property
    def rewards(self):
        return [TaskReward.get(pk) for pk in self.rewards_int.strip().split(",") if pk]



    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = self.id
        dicts["rewards"] = [_reward.to_dict() for _reward in self.rewards]
       
        del dicts["id"]
        return dicts





class SevenDaysHalfPrice(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"七天半价购"
    #suitId = models.IntegerField(u"套装Ｉｄ", default=0)
    #iconId = models.IntegerField(u"头像", default=0)
    #itemNameMul = models.CharField(u"道具名字多语言,", max_length=200, default="")
    itemCost = models.IntegerField(u"物品花费", default=0)
    #itemType = models.IntegerField(u"物品分类", default=0)
    #count = models.IntegerField(u"数量", default=0)
    rewardId = models.CharField(u"奖励", max_length=200, default="")

    @memoized_property
    def reward(self):
        from rewards.api import get_commonreward
        return get_commonreward(self.rewardId)


    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["pk"] = self.id

        del dicts["id"]
        return dicts




class TaskReward(RewardsBase):
    SHEET_NAME = u"任务奖励"
