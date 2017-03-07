#-*- encoding:utf-8 -*-
from activity.models import Activity, ActivityRule, GiftPackage,ActivityReward

def update_activity_cache():
    Activity.create_cache()
    ActivityRule.create_cache()
    GiftPackage.create_cache()
    ActivityReward.create_cache()

def get_activity(activity_id):
    '''
    获取章节
    '''
    return Activity.get(activity_id)

def get_activities():
    '''
    获取所有章节
    '''
    return Activity.get_all_list()

def get_open_activities(player):
    '''
    获取所有开启的活动
    '''
    activities = get_activities()
    open_activities = [activity for activity in activities if activity.isOpen(player.userid)]
    return open_activities

def get_activity_by_type(player, activityType):
    '''
    根据类型获取活动(开启的)
    '''
    activities = get_all_activities()
    for activity in activities:
        if activity.category == activityType:
            if activity.isOpen(player.userid):
                return activity
    return None
