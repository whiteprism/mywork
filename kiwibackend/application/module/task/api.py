# -*- coding: utf-8 -*-
from task.models import TaskCondition, Task, DailyTask, SevenDaysTask, TaskReward, DailyTaskActivity, SevenDaysHalfPrice

def update_task_cache():
    Task.create_cache()
    DailyTask.create_cache()
    TaskCondition.create_cache()
    SevenDaysTask.create_cache()
    TaskReward.create_cache()
    DailyTaskActivity.create_cache()
    SevenDaysHalfPrice.create_cache()

def get_task(pk):
    return Task.get(int(pk))

def get_tasks():
    return Task.get_all_list()

def get_init_tasks():
    return Task.get_init_tasks() 

def get_dailytask(pk):
    return DailyTask.get(int(pk))

def get_dailytasks():
    return DailyTask.get_all_list()

def get_init_dailytasks():
    return DailyTask.get_init_dailytasks()

def get_seven_days_task(pk):
    return SevenDaysTask.get(int(pk))

def get_seven_days_tasks():
    return SevenDaysTask.get_all_list()

def get_init_seven_days_tasks():
    return SevenDaysTask.get_init_seven_days_tasks()

def get_dailytask_activity(pk):
    return DailyTaskActivity.get(int(pk))

def get_dailytask_activities():
    return DailyTaskActivity.get_all_list()


def get_sevenDaysHalfPrice(pk):
    return SevenDaysHalfPrice.get(int(pk))

def get_sevenDaysHalfPrices():
    return SevenDaysHalfPrice.get_all_list()



SevenDaysHalfPrice










