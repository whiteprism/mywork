# -*- coding: utf-8 -*-
from experiment.models import Experiment
import datetime
from experiment.static import *
from module.utils import datetime_to_unixtime

def get_experiments():
    return Experiment.get_all_list()

def get_game_experiment():
    return get_experiment(GAME_EXPERIMENT_ID)

def get_experiment(experiment_name):
    '''
    获取实验
    '''
    return Experiment.get(experiment_name)

def get_active_experiments(userid):
    game_experiment = get_game_experiment()
    active_experiment_names = game_experiment.values.get("activeExperiments", [])
    active_experiments = {}
    for experiment_name in active_experiment_names:
        experiment = get_experiment(experiment_name)
        if experiment:
            active_experiments[experiment_name] = {
                "startedAt": datetime_to_unixtime(experiment.started_at),
                "endedAt": datetime_to_unixtime(experiment.ended_at),
                "inWhites": userid in (experiment.whites + game_experiment.whites),
                "inBlacks": userid in (experiment.blacks + game_experiment.blacks),
                "name":experiment_name, 
#                "values": {} if experiment.pk == GAME_EXPERIMENT_ID else experiment.values
            }

    return active_experiments

def check_player_in_experiment_by_experiment(userid, experiment):
    '''
    检查用户是否在实验中
    '''
    if not userid:
        return False

    game_experiment = get_game_experiment()
    active_experiment_names = game_experiment.values.get("activeExperiments", [])

    if not experiment or type(experiment) is not Experiment:
        return False

    userid = int(userid)

    #黑名单     
    blacklist = game_experiment.blacks + experiment.blacks
    
    #黑名单中的用户永远不在实验中
    if userid in blacklist:
        return False

    now = datetime.datetime.now()

    #白名单
    whitelist = game_experiment.whites + experiment.whites
    
    #白名单用户永远在试验中（实验过期除外）
    if userid in whitelist:
        #只看过期时间，不看开始时间
        if now < experiment.ended_at:
            return True 

    if experiment.is_alltime and experiment.started_at <= now <= experiment.ended_at:
        return True


    if experiment.is_weektime:
        if now.isoweekday() in experiment.weekdays:
            if experiment.week_started_at <= now.time() <= experiment.week_ended_at:
                return True

    return False
    
def check_player_in_experiment_by_experimentname(userid, experiment_name):
    '''
    检查用户是否在实验中
    '''
    experiment = get_experiment(experiment_name)
    if experiment:
        return check_player_in_experiment_by_experiment(userid, experiment)
    else:
        return False

