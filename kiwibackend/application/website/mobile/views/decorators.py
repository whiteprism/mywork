# -*- encoding:utf8 -*-
from django.conf import settings
from importlib import import_module
import time, datetime
from messages.maps.child import ChildMap
from messages.http.common_response import CommonResponse
from messages.http.common_request import CommonRequest
from messages.userdata.viewUser import ViewUser
from messages.userdata.viewModify import ViewUpdate, ViewDelete
import cPickle
from player.api import create_player, get_player_by_userid
from playerinstance.api import get_update_instance_dict
from module.common.static import ErrorID, Static
from module.mail.api import get_mail
from module.battlerecords.api import get_record
from module.experiment.api import get_active_experiments, get_game_experiment
from module.utils import delta_time
import md5

def deco_root(view_func):
    def _handle(request, response):
        player = get_player_by_userid(request.common_request.playerId, request.common_request.serverid)
        if not player:
            player = create_player(request)

        request.player = player
        player.request = request
        player.response = response
        client_time = int(request.common_request.clientTime)
        player.set("client_time" ,client_time)
        player.set("current_client_time", client_time)
        player.set("server_time" , int(time.time()))
        player.set("deviceId",request.common_request.deviceId)
        player.dailyCheck()
        # 这里是调用方法的实际地方
        response = view_func(request, response)
        _modify_handler(request, response)

        session = import_module(settings.SESSION_ENGINE).SessionStore()
        session["userid"] = player.userid
        session.set_expiry(3599) #一个小时内没有登录token失效 
        timestamp = int(request.http_request.META.get("HTTP_TIMESTAMP",0))
        session["requestTimeStamp"] = int(timestamp)
        # session["lastResponse"] = cPickle.dumps(response)
        session.save()
        response.logic_response.set("sessionId", session.session_key)
        game_experiment = get_game_experiment()
        response.common_response.set("vvv",int(game_experiment.values.get("vvv", 0)))
        response.common_response.player.set("experiments", get_active_experiments(player).values())
        player.update()
        return response
    return _handle

def require_player(view_func):
    def _handle(request, response):
        session_id = request.common_request.sessionId
        request.session = import_module(settings.SESSION_ENGINE).SessionStore(session_id)
        expiry_age = request.session.get_expiry_age()
        #print "expiry_age is %s"  % expiry_age 

        #时间太久没有登陆，请重新登陆
        if expiry_age <= 0 or  expiry_age > 3600:
            request.session.flush()
            response.common_response.set("success", False)
            response.common_response.set("errorCode", ErrorID.ERROR_LOGIN_TIMEOUT)
            return response

        #用户登陆错误
        if int(request.session.get('userid', 0)) != int(request.common_request.playerId):
            request.session.flush()
            response.common_response.set("success", False)
            response.common_response.set("errorCode", ErrorID.ERROR_LOGIN_ERROR_USER)
            return response

        #掉线重连检查
        timestamp = int(request.http_request.META.get("HTTP_TIMESTAMP",0))
        if not timestamp:
            response.common_response.set("success", False)
            response.common_response.set("errorCode", ErrorID.ERROR_SIGN)
            return response

        if int(request.session["requestTimeStamp"]) == int(timestamp):
            return cPickle.loads(request.session["lastResponse"])
        
        player = get_player_by_userid(request.common_request.playerId, request.common_request.serverid)
        player.request = request
        player.response = response
        token = request.http_request.META.get("HTTP_TOKEN","").replace("-", "").lower()
        seed = request.common_request.seed

        #设备在其他机器登陆
        if player.deviceId != request.common_request.deviceId:
            #print "player deviceId is %s and request deviceId is %s" % (player.deviceId, request.common_request.deviceId)
            response.common_response.set("success", False)
            response.common_response.set("errorCode", ErrorID.ERROR_ACCOUNT_LOGIN_ON_OTHER_DEVICE)
            return response

        if not player.check_md5(seed) or md5.md5(request.request_body).hexdigest() != token:
           response.common_response.set("success", False)
           response.common_response.set("errorCode", ErrorID.ERROR_SIGN)
           return response
        player.use_md5Seed(seed)


        #封号检查
        now = datetime.datetime.now()
        if delta_time(now, player.banAt) > 1:
            #时间差大于1秒
            response.common_response.set("success", False)
            response.common_response.set("errorCode", ErrorID.ERROR_BANNED)
            return response

        if not request.logic_request.timeDelay:
            #yoyprint("check time delay")
            #加速器检查 or 修改时间检查
            client_time = int(request.common_request.clientTime) #前端时间
            delta_server_time =  int(time.time()) - player.server_time
            delta_client_time =  client_time - player.client_time

            #修改时间
            if delta_client_time < 0 or player.current_client_time > client_time:
                response.common_response.set("success", False)
                response.common_response.set("errorCode", ErrorID.ERROR_TIME_CHANGED_ERROR)
                return response

            #用户使用加速器
            if delta_client_time - delta_server_time > 60 :
                response.common_response.set("success", False)
                response.common_response.set("errorCode", ErrorID.ERROR_TIME_ERROR)
                return response

            player.set("current_client_time",  client_time)

        request.player = player
        if player.tutorial["guideGid"] == Static.TUTORIAL_ID_ELITE_INSTANCE and player.tutorial["status"] == 1:
            player.tutorial_complete()

        if request.common_request.powerRank:
            player.setPowerRank(request.common_request.powerRank)

        response = view_func(request, response)
        if request.common_request.maxFiveHeroPower > 0:
            player.seven_days_task_going(category=Static.SEVEN_TASK_CATEGORY_BATTLE_POWER, number=int(request.common_request.maxFiveHeroPower), is_incr=False, with_top=True, is_series=True)

        #整点请求
        now = datetime.datetime.now()
        next_hour = now + datetime.timedelta(seconds=3600)
        next_int_hour = datetime.datetime(next_hour.year, next_hour.month, next_hour.day, next_hour.hour)
        serverIntCDTime = (next_int_hour - now).total_seconds() + 1
        response.common_response.set("serverIntCDTime", int(serverIntCDTime))

        player.dailyCheck()
        #副本更新 普通副本 and 精英副本
        instancesDict = get_update_instance_dict(player)
        
        if instancesDict:
            response.common_response.player.set("instance", instancesDict)

        game_experiment = get_game_experiment()
        if int(game_experiment.values.get("vvv", -1)) != request.common_request.vvv:
            response.common_response.set("vvv",int(game_experiment.values.get("vvv", 0)))
            response.common_response.player.set("experiments", get_active_experiments(player).values())

        response.common_response.player.set("level", player.level)
        response.common_response.player.set("xp", player.xp)
        response.common_response.player.set("gold", player.gold)
        response.common_response.player.set("wood", player.wood)
        response.common_response.player.set("diamond", player.yuanbo)
        response.common_response.player.set("couragePoint", player.couragepoint)
        response.common_response.player.set("power", player.power)
        response.common_response.player.set("stamina", player.stamina)
        response.common_response.player.set("dailyTaskActivity", player.dailyTaskActivity)
        response.common_response.player.set("activityBoxIds", player.activityBoxIds)
        response.common_response.player.set("activityValue", player.activityValue)
        response.common_response.player.set("towerGold", player.towerGold)

        response.common_response.player.set("daysFromcreated", player.daysFromcreated)
        #response.common_response.player.set("fireBuff", player.fireBuff)
        response.common_response.player.set("completeTaskList", [(int(taskId), status) for taskId, status in player.completeSevenTasks.items()])

        response.common_response.player.set("powerCDTime",player.next_power_time)
        response.common_response.player.set("staminaCDTime", player.next_stamina_time)
        response.common_response.player.set("weekCardLeftDay", player.week_card_left_day)
        response.common_response.player.set("monthCardLeftDay", player.month_card_left_day)
        response.common_response.player.set("permanentCardActivity", player.permanent_card_is_activity)
        response.common_response.player.set("hasUnReadMails", player.has_unread_mails)
        response.common_response.player.set("seeds", player.md5Seeds)
        response.common_response.set("serverTime", int(time.time()))
        if player.tutorial_change:
            response.common_response.player.set("tutorial", player.tutorial)

        if player.armies_change:
            player.response.common_response.player.set("soldiers", player.armies.to_dict())

        if player.levelup and player.level == Static.PVP_LEVEL:
            player.arenashop.refresh_auto()
            response.common_response.player.set("honorShop", player.arenashop.to_dict())
            response.common_response.player.set("arena", player.PVP.to_dict())

        if player.levelup and player.level == Static.SIEGE_LEVEL:
            player.SiegeBattle.refresh_auto()
            response.common_response.player.set("siegeBattle", player.SiegeBattle.to_dict())

        if player.PVP_change and player.isOpenArena:
            response.common_response.player.set("arena", player.PVP.to_dict())

        _modify_handler(request, response)
        request.session.set_expiry(3599) #一个小时内没有登录token失效
        #用户数据保存
        player.update()
        #保存上一次操作数据
        request.session["requestTimeStamp"] = int(timestamp)
        request.session["lastResponse"] = cPickle.dumps(response)
        request.session.save()
        return response

    return _handle

def handle_common(view_func):
    def _handle(request, response):
        view_name = request.view_name



        child_map = ChildMap()
        #response data
        common_response = CommonResponse()
        player = ViewUser()
        common_response.set("player", player)
        common_response.set("success", True)
        child_map.set("commonResponse", common_response)
        
        LogicResponse = getattr(import_module("website.messages.http.%s_response" % view_name), "%sResponse" % (view_name[0].upper()+view_name[1:]))
        logic_response = LogicResponse()
        child_map.set("response", logic_response)
        response.logic_response = logic_response

        response.set(view_name, child_map)
        response.common_response = common_response

        #request data
        common_request = CommonRequest()
        common_request.for_request(getattr(request, view_name)["commonRequest"])

        LogicRequest = getattr(import_module("website.messages.http.%s_request" % view_name), "%sRequest" % (view_name[0].upper()+view_name[1:]))
        logic_request = LogicRequest()
        logic_request.for_request(getattr(request, view_name)["request"])
        #if request.view_name != "init":
        #    yoyprint(u"%s%s%s" %(u"#"*10, u"Request Params START", u"#"*10))
        #    for k,v in getattr(request, view_name)["request"].items():
        #        try:
        #            yoyprint(u"%s => %s" % (k,v))
        #        except:
        #            pass
        #    yoyprint(u"%s%s%s" %(u"#"*10, u"Request Params E N D", u"#"*10))
        #else:
        #    yoyprint(u"%s%s%s" %(u"#"*10, u"Request Params START", u"#"*10))
        #    for k,v in getattr(request, view_name)["commonRequest"].items():
        #        yoyprint(u"%s => %s" % (k,v))
        #    yoyprint(u"%s%s%s" %(u"#"*10, u"Request Params E N D", u"#"*10))
        
        request.common_request = common_request
        request.logic_request = logic_request
        response = view_func(request, response)

        return response
    return _handle

def _modify_handler(request, response):
    if  type(response) != dict and hasattr(request, "player"):
        # modifydata = request.player.modifydata()
        heroes = _hero_handler(request, response)
        heroteams = _heroteam_handler(request, response)
        souls  = _soul_handler(request, response)
        equips = _equip_handler(request, response)
        buildings = _building_handler(request, response)
        #gems = _gem_handler(request, response)
        #gemfragments = _gemfragment_handler(request, response)
        items = _item_handler(request, response)
        buyrecords = _buyrecords_handler(request, response)
        artifacts = _artifacts_handler(request, response)
        dailytasks = _dailytasks_handler(request, response)
        sevenDaystasks = _seven_days_tasks_handler(request, response)
        tasks = _tasks_handler(request, response)
        equipfragments = _equipfragments_handler(request, response)
        artifactfragments = _artifactfragments_handler(request, response)
        buildingfragments = _buildingfragments_handler(request, response)
        buildingplants = _buildingplant_handler(request, response)
        activities = _activity_handler(request, response)
        mails = _mails_handler(request, response)
        battlerecords = _battlerecords_handler(request, response)
        rampartsoldiers = _rampartsoldiers_handler(request, response)

        # if modifydata:
        #     modifydata.delete()
        #modify_datas = [heroes, souls, equips, buildings, gems, gemfragments, items, buyrecords, artifacts, dailytasks, tasks, equipfragments, artifactfragments, activities, mails]
        modify_datas = [heroes,heroteams,souls, equips, buildings, items, buyrecords, artifacts, dailytasks, tasks, sevenDaystasks, equipfragments, artifactfragments, buildingfragments, buildingplants, activities, mails, battlerecords, rampartsoldiers]
        for m in modify_datas:
            if "update" in m and m["update"]:
                if not response.common_response.update:
                    response.common_response.set("update", ViewUpdate())
                response.common_response.update.set(m["name"], m["update"])

            if "delete" in m and m["delete"]:
                if not response.common_response.delete:
                    response.common_response.set("delete", ViewDelete())
                response.common_response.delete.set(m["name"], m["delete"])

def _hero_handler(request, response):
    player = request.player
    heroes = {
        "name": "heroes",
        "update":[],
    }
    for pk in player._update_list["heroes"]:
        heroes["update"].append(player.heroes.get(pk).to_dict())
        
    return heroes


def _heroteam_handler(request, response):
    player = request.player
    heroTeams = {
        "name": "heroTeams",
        "update":[],
    }
    for pk in player._update_list["heroTeams"]:
        heroTeams["update"].append(player.heroteams.get(pk).to_dict())

    return heroTeams
    
def _artifacts_handler(request, response):
    player = request.player
    artifacts = {
        "name": "artifacts",
        "update":[],
        "delete":[],
    }
    for pk in player._update_list["artifacts"]:
        artifacts["update"].append(player.artifacts.get(pk).to_dict())
        
    for pk in player._delete_list["artifacts"]:
        artifacts["delete"].append({"id": pk})

    return artifacts

def _soul_handler(request, response):
    player = request.player
    souls = {
        "name": "souls",
        "update":[],
        "delete":[],
    }
    for pk in player._update_list["souls"]:
        souls["update"].append(player.souls.get(pk).to_dict())
        
    for pk in player._delete_list["souls"]:
        souls["delete"].append({"soulId": pk})
    return souls

def _equip_handler(request, response):
    player = request.player
    equips = {
        "name": "equips",
        "update":[],
        "delete":[],
    }
    for pk in player._update_list["equips"]:
        equips["update"].append(player.equips.get(pk).to_dict())
        
    for pk in player._delete_list["equips"]:
        equips["delete"].append({"id": pk})

    return equips

def _building_handler(request, response):
    player = request.player
    buildings = {
        "name": "buildings",
        "update":[],
        "delete":[],
    }
    for pk in player._update_list["buildings"]:
        buildings["update"].append(player.buildings.get(pk).to_dict())
    for pk in player._delete_list["buildings"]:
        buildings["delete"].append({"id": pk})
    return buildings


def _buildingfragments_handler(request, response):
        
    player = request.player
    fragments = {
        "name": "buildingFragments",
        "update":[],
        "delete":[],
    }
    for pk in player._update_list["buildingFragments"]:
        fragments["update"].append(player.buildingfragments.get(pk).to_dict())

    for fragment_id in player._delete_list["buildingFragments"]:
        fragments["delete"].append({"buildingFragmentId": fragment_id})
    return fragments
    
def _buildingplant_handler(request, response):
    player = request.player
    plants = {
        "name": "buildingPlants",
        "update":[],
        "delete":[],
    }
    for pk in player._update_list["buildingPlants"]:
        plants["update"].append(player.buildingplants.get(pk).to_dict())
    for pk in player._delete_list["buildingPlants"]:
        plants["delete"].append({"id": pk})
    return plants

def _item_handler(request, response):
    player = request.player
    items = {
        "name": "items",
        "update":[],
        "delete":[],
    }
    for pk in player._update_list["items"]:
        items["update"].append(player.items.get(pk).to_dict())
        
    for pk in player._delete_list["items"]:
        items["delete"].append({"id": pk})
    return items

def _buyrecords_handler(request, response):
    player = request.player
    buyRecords = {
        "name": "buyRecords",
        "update":[],
    }
    for pk in player._update_list["buyRecords"]:
        buyRecords["update"].append(player.buyrecords.get(pk).to_dict())
        
    return buyRecords

def _activity_handler(request, response):
    player = request.player
    activities = {
        "name": "activities",
        "update":[],
    }
    for pk in player._update_list["activities"]:
        activities["update"].append(player.activities.get(pk).to_dict())

    return activities 

def _dailytasks_handler(request, response):
    player = request.player
    dailytasks = {
        "name": "dailytasks",
        "update":[],
        "delete":[],
    }
    for category in player._update_list["dailytasks"]:
        dailytask = player.dailytask_dict(category)
        if dailytask:
            dailytasks["update"].append(dailytask)

    dailytasks["delete"] = [{"taskGid": _k} for _k in player._delete_list["dailytasks"]]
    return dailytasks

def _seven_days_tasks_handler(request, response):
    player = request.player
    sevenDaystasks = {
        "name": "sevenDaystasks",
        "update":[],
        "delete":[],
    }
    for category in player._update_list["sevenDaystasks"]:
        sevenDaystask = player.seven_days_task_dict(category)
        if sevenDaystask:
            sevenDaystasks["update"].append(sevenDaystask)

    sevenDaystasks["delete"] = [{"taskGid": _k} for _k in player._delete_list["sevenDaystasks"]]
    return sevenDaystasks
        
def _tasks_handler(request, response):
    player = request.player
    tasks = {
        "name": "tasks",
        "update":[],
        "delete":[],
    }
    for category in player._update_list["tasks"]:
        task = player.task_dict(category)
        if task:
            tasks["update"].append(task)

    tasks["delete"] = [{"taskGid": _k} for _k in player._delete_list["tasks"]]
    return tasks 

def _equipfragments_handler(request, response):
    player = request.player
    fragments = {
        "name": "equipFragments",
        "update":[],
        "delete":[],
    }
    for pk in player._update_list["equipFragments"]:
        fragments["update"].append(player.equipfragments.get(pk).to_dict())
        
    for fragment_id in player._delete_list["equipFragments"]:
        fragments["delete"].append({"equipFragmentId": fragment_id})

    return fragments

def _artifactfragments_handler(request, response):
        
    player = request.player
    fragments = {
        "name": "artifactFragments",
        "update":[],
        "delete":[],
    }
    for pk in player._update_list["artifactFragments"]:
        fragments["update"].append(player.artifactfragments.get(pk).to_dict())

    for fragment_id in player._delete_list["artifactFragments"]:
        fragments["delete"].append({"artifactFragmentId": fragment_id})
    return fragments

def _mails_handler(request, response):
    player = request.player
    mails = {
        "name": "mails",
        "update":[],
        "delete":[],
    }

    for pk in player._update_list["mails"]:
        mails["update"].append(get_mail(pk).to_dict())
        
    for pk in player._delete_list["mails"]:
        mails["delete"].append({"id": pk})

    return mails


def _battlerecords_handler(request, response):
    player = request.player
    battlerecords = {
        "name": "battlerecords",
        "update":[],
        "delete":[],
    }

    for pk in player._update_list["battlerecords"]:
        battlerecords["battlerecords"].append(get_record(pk).to_dict())

    for pk in player._delete_list["battlerecords"]:
        battlerecords["delete"].append({"id": pk})

    return battlerecords

def _rampartsoldiers_handler(request, response):
    player = request.player
    soldiers = {
        "name": "rampartSoldiers",
        "update":[],
        "delete":[],
    }

    for pk in player._update_list["rampartSoldiers"]:
        soldiers["update"].append(player.rampartSoldiers.get(pk).to_dict())
        
    for pk in player._delete_list["rampartSoldiers"]:
        soldiers["delete"].append({"id": pk})

    return soldiers
