# -*- coding: utf-8 -*
from django.contrib.admin.views.decorators import  staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from gameconfig.api import get_models, get_model,check_func
from module.server.api import get_server_by_request
import urllib, urllib2
import pymongo
from django.conf import settings
import datetime

client = pymongo.MongoClient(settings.MONGO_HOST,settings.MONGO_PORT)

@staff_member_required
def get_action_info(request):
    '''
    查看玩家行为数据
    '''
    playerId = request.POST.get("player_id","")
    action_dict = dict(request.POST.items())
    del action_dict["player_id"]
    del action_dict["start_time"]
    del action_dict["end_time"]
    server = get_server_by_request(request)
    #db = client["%s_s%s" % (settings.PLATFORM_PREFIX, server.id)]
    startTime = request.POST.get("start_time","")
    endTime = request.POST.get("end_time","")
    player_id = int(server.id) * 1000000000 + int(playerId)
    err_message = u""

    try:
        start_datetime = datetime.datetime.strptime(startTime,'%Y-%m-%d %H:%M')
        end_datetime = datetime.datetime.strptime(endTime,'%Y-%m-%d %H:%M')
        if end_datetime <= start_datetime:
            err_message = u"开始时间必须小于结束时间！"
    except:
        err_message = u"请输入正确的开始时间和结束时间！"

    datas = []
    if not err_message:
        db = client["%s_s%s" % (settings.PLATFORM_PREFIX, server.id)]

        log_date = start_datetime.date()
        start_date = start_datetime.date()
        end_date = end_datetime.date()
        list_date = start_date
        date_list = [start_date]
        if list_date < end_date:
            list_date += datetime.timedelta(days = 1)
            date_list.append(list_date)
        for date in date_list:
            table = db["log_%s%s%s" % (date.year, str(date.month).rjust(2, "0"), str(date.day).rjust(2, "0"))]
            for action in action_dict.keys():
                if date == start_date == end_date:
                    data = list(table.find({"user_id":str(player_id), "action":str(action), "category":{"$in": request.POST.getlist(str(action))}, "action_time":{"$gte": startTime, "$lte": endTime}}).sort("action_time",pymongo.ASCENDING))
                elif date == start_date:
                    data = list(table.find({"user_id":str(player_id), "action":str(action), "category":{"$in": request.POST.getlist(str(action))}, "action_time":{"$gte": startTime}}).sort("action_time",pymongo.ASCENDING))
                elif date == end_date:
                    data = list(table.find({"user_id":str(player_id), "action":str(action), "category":{"$in": request.POST.getlist(str(action))}, "action_time":{"$lte": endTime}}).sort("action_time",pymongo.ASCENDING))
                else:
                    data = list(table.find({"user_id":str(player_id), "action":str(action), "category":{"$in": request.POST.getlist(str(action))}}).sort("action_time",pymongo.ASCENDING))
                datas.extend(data)

        for action_data in datas:
            action_data["message"] = eval(action_data["message"])
            action_data["info"] = action_data["message"].get("info","")
            del action_data["message"]["info"]
            # action_data["message"]["before"] = action_data["message"].get("before",-1)
            # action_data["message"]["after"] = action_data["message"].get("after",-1)

        resdata = {
            "ret":True,
            "actions_info":datas,
            }
        print datas
    else:
        resdata = {
        "ret":False,
        "msg":err_message,
        }

    ctxt = RequestContext(request,resdata)

    return render_to_response("action/action_result.html", ctxt)
