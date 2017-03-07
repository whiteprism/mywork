# -*- coding: utf-8 -*-

#from module.playerPVP.api import send_pvp_rewards,send_pvp_daily_rewards,send_pvp_rank


def cron_send_pvp_rewards(signum):
    send_pvp_rewards()
    print "send_pvp_rewards ok"

def cron_send_pvp_daily_rewards():
    send_pvp_daily_rewards()
    print "send daily pvp rewards ok"

def cron_send_pvp_rank():
    cron_send_pvp_rank()
    print "send pvp rank ok"


jobs = [ 
#        {
#            "name" : cron_send_pvp_rewards,
#            "time": [0, 9, -1, -1, 1], #minute, hour, day, month, weekday, "-1" means "all"
#            },
#
#        
#        
#        {
#            "name" : cron_send_pvp_daily_rewards,
#            "time": [0, 9, -1, -1, -1], #minute, hour, day, month, weekday, "-1" means "all"
#            },
#
#        {
#            "name" : cron_send_pvp_rank,
#            "time": [0, 9, -1, -1, -1], #minute, hour, day, month, weekday, "-1" means "all"
#            },
#        
]
