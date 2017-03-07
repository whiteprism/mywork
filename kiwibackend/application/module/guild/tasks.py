# -*- coding: utf-8 -*-
from module.celerytask import TaskSchedulerObj
from django.conf import settings
from .api import get_guildmaxinfo
import datetime, time
from module.player.api import get_player, get_players_by_ids
from module.mail.api import send_system_mail
from module.common.static import Static
import simplejson
class GuilTask(object):
    AUCTION_BALANCE = "guild.tasks.task_balance_guildauctionmaxinfo"

def _task_balance_guildauctionmaxinfo_key(id):
    return "%s-%s" % (GuilTask.AUCTION_BALANCE, id)

def task_add_balance_guildauctionmaxinfo(maxinfo):
    task_at = maxinfo.aucEndAt 
    TaskSchedulerObj.add_crontab_scheduler(GuilTask.AUCTION_BALANCE, {"minute": task_at.minute, "hour": task_at.hour, "day_of_month":task_at.day, "month_of_year": task_at.month}, (maxinfo.id,))

def task_del_balance_guildauctionmaxinfo(id):
    TaskSchedulerObj.delete(_task_balance_guildauctionmaxinfo_key(id))

@settings.CELERY_APP.task
def task_balance_guildauctionmaxinfo(id):
    """
    公会拍卖结算
    """
    task_del_balance_guildauctionmaxinfo(id)
    maxinfo = get_guildmaxinfo(id)
    msg = ""
    if not maxinfo:
        msg = "guild auction balance maxinfo %s not existed" % id
    else:
        if maxinfo.timeLeft > 0 and abs(maxinfo.timeLeft - int(time.time()))> 120: #超过两分钟不结算
            task_add_balance_guildauctionmaxinfo(maxinfo)
            msg = "guild auction balance error , right at %s" % str(maxinfo.aucEndAt)
        else:
            auctionInfos = zip(maxinfo.playerIds, maxinfo.prices)
            auctionInfos.sort(lambda x,y : cmp(y[1], x[1]))
            successContents = []#竞拍成功内容
            successContents.append({
                "content": "fytext_300752",
            })
            successContents.append({
                "content": "fytext_300753",
                "paramList": [str(maxinfo.maxPrice)],
            })
            successContents.append({
                "content": "fytext_300754",
            })

            failContents = []#竞拍失败内容
            failContents.append({
                "content": "fytext_300756",
                "paramList": [str(maxinfo.auctionReward.reward.name)],
            })


            players = get_players_by_ids(maxinfo.playerIds)

            for playerId, price in auctionInfos:
                player = players[playerId]
                successContents.append({
                    "content": "fytext_301170",
                    "paramList": [player.name, str(price)]
                })
                failContents.append({
                    "content": "fytext_301170",
                    "paramList": [player.name, str(price)]
                })
            failContents.append({
                "content": "fytext_300757",
            })
            for playerId, price in auctionInfos:
                player = players[playerId]
                rewards = []
                if playerId == maxinfo.maxPlayerId:
                    rewards.append(maxinfo.auctionReward.reward.to_dict())
                    send_system_mail(player, None, "fytext_300751", contents=successContents, rewards=rewards)
                else:
                    rewards.append({"type": Static.GUILDGOLD_ID, "count": price})
                    send_system_mail(player, None, "fytext_300755", contents=failContents, rewards=rewards)

            maxinfo.delete()
            msg = "guild auction balance success %s" % simplejson.dumps(auctionInfos) 

    return msg

