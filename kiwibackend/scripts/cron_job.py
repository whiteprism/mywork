# -*- coding: utf-8 -*-

#from module.playerPVP.api import send_pvp_rewards,send_pvp_daily_rewards,send_pvp_rank
from module.playerPVP.api import send_daily_pvp_rewards,send_weekly_pvp_rewards, init_weekly_pvp_data


def cron_send_daily_pvp_rewards(a):
    send_daily_pvp_rewards()
    print "send_daily_pvp_rewards ok"

def cron_send_weekly_pvp_rewards(a):
    send_weekly_pvp_rewards()
    print "send_weekly_pvp_rewards ok"

def cron_init_weekly_pvp_data(a):
    init_weekly_pvp_data()
    print "init_weekly_pvp_data ok"


jobs = [ 
        {
            "name" : cron_send_daily_pvp_rewards,
            "time": [15, 9, -1, -1, -1], #minute, hour, day, month, weekday, "-1" means "all"
        },
        {
            "name" : cron_send_weekly_pvp_rewards,
            "time": [15, 9, -1, -1, 1], #minute, hour, day, month, weekday, "-1" means "all"
        },

        {
            "name" : cron_init_weekly_pvp_data,
            "time": [15, 9, -1, -1, 1], #minute, hour, day, month, weekday, "-1" means "all"
            },
        
]
