# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext 
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from module.player.api import *
from module.playeritem.api import *
from module.item.api import *
from module.playerhero.api import *
from module.soul.api import *

from module.equip.api import *
from module.playerequip.api import acquire_equip, acquire_equipfragment

from module.artifact.api import *
from module.playerartifact.api import *

from module.building.api import *
from module.playerbuilding.api import *

from module.playersoul.api import acquire_soul
from submodule.fanyoy import short_data
from module.levelconf.api import get_level
from django.conf import settings

def index(request):
    return render_to_response("debug/index.html")

def get_player_by_id_or_str(player_code):

    if len(player_code) >= 8:

        player = Player.objects.get(id=int(short_data.decompress(str.upper(str(player_code)))))
    else:
        player = get_player_by_userid(int(player_code), settings.SERVERID)

    return player

def set_level_and_xp(request):
    player_code = request.REQUEST.get("player_code")
    level = request.REQUEST.get("level", 0)
    xp = request.REQUEST.get("xp", 0)
    addxp = request.REQUEST.get("addxp", 0)
    player = get_player_by_id_or_str(player_code)

    player.add_xp(int(addxp))
    if level:
        if not get_level(level):
            return HttpResponseRedirect(reverse("mobile_debug_index"))
        player.set("level",int(level))
    if xp:
        player.set("xp", int(xp))
    player.update()
    return HttpResponseRedirect(reverse("mobile_debug_index"))

def add_power_and_sp(request):
    player_code = request.REQUEST.get("player_code")
    power = request.REQUEST.get("power", 1)
    sp = request.REQUEST.get("sp", 0)
    player = get_player_by_id_or_str(player_code)

    player.add_power(int(power))
    player.add_stamina(int(sp))

    player.update()
    return HttpResponseRedirect(reverse("mobile_debug_index"))

def set_vip(request):
    player_code = request.REQUEST.get("player_code")
    level = request.REQUEST.get("level", 1)
    count = request.REQUEST.get("count", 0)
    player = get_player_by_id_or_str(player_code)
    if not count:
        count = 0
    if not level:
        level = 0
    player.vip["chargeCount"] = int(count)
    player.vip["vipLevel"] = int(level)
    player.set_update("vip")
    player.update()
    return HttpResponseRedirect(reverse("mobile_debug_index"))

def set_tutorial(request):
    player_code = request.REQUEST.get("player_code")
    tutorial_code = request.REQUEST.get("code", 100)
    tutorial_status = request.REQUEST.get("status", 1)
    player = get_player_by_id_or_str(player_code)
    player.tutorial = {"guideGid": int(tutorial_code), "status":int(tutorial_status)}
    player.set_update("tutorial")
    player.firstIn = 0
    player.set_update("firstIn")
    player.update()
    return HttpResponseRedirect(reverse("mobile_debug_index"))

def add_item(request):
    player_code = request.REQUEST.get("player_code")
    player = get_player_by_id_or_str(player_code)
    item_id = request.REQUEST.get("item", 0)
    number = request.REQUEST.get("number", 0)
    item = get_item(item_id)
    if item:
        acquire_item(player, item, number=int(number), info="debug")
        player.update()
    
    return HttpResponseRedirect(reverse("mobile_debug_index"))

def add_equip(request):
    player_code = request.REQUEST.get("player_code")
    player = get_player_by_id_or_str(player_code)
    equip_id = request.REQUEST.get("equip", 0)
    number = request.REQUEST.get("number", 0)
    equip = get_equip(equip_id)
    if equip:
        for i in range(0, int(number)):
            acquire_equip(player, equip, info="debug")

        player.update()

    
    return HttpResponseRedirect(reverse("mobile_debug_index"))

def add_equipfragment(request):
    player_code = request.REQUEST.get("player_code")
    player = get_player_by_id_or_str(player_code)
    equipfragment_id = request.REQUEST.get("equipfragment_id", 0)
    number = request.REQUEST.get("number", 0)
    equipfragment = get_equipfragment(equipfragment_id)
    if equipfragment:
        acquire_equipfragment(player, equipfragment.pk, int(number))
        player.update()
    
    return HttpResponseRedirect(reverse("mobile_debug_index"))

def add_artifact(request):
    player_code = request.REQUEST.get("player_code")
    player = get_player_by_id_or_str(player_code)
    artifact_id = request.REQUEST.get("artifact_id", 0)
    fragment_id = request.REQUEST.get("artifactFragment_id", 0)

    number = request.REQUEST.get("number", 0)

    if fragment_id:
        fragment = get_artifactfragment(fragment_id)
        if fragment:
            acquire_artifactfragment(player, fragment, int(number))

    if artifact_id:
        artifact = get_artifact(artifact_id)
        if artifact:
            for i in range(0, int(number)):
                acquire_artifact(player, artifact, info="debug")
    player.update()
    return HttpResponseRedirect(reverse("mobile_debug_index"))

def add_soul(request):
    player_code = request.REQUEST.get("player_code")
    player = get_player_by_id_or_str(player_code)
    soul_id = request.REQUEST.get("soul_id", 0)

    soul = get_soul(int(soul_id))
    number = request.REQUEST.get("number", 0)
    if soul:
        acquire_soul(player, int(soul_id), int(number), "debug")
        player.update()

    return HttpResponseRedirect(reverse("mobile_debug_index"))

def add_warrior(request):
    player_code = request.REQUEST.get("player_code")
    player = get_player_by_id_or_str(player_code)
    number = request.REQUEST.get("number", 0)
    card_id = request.REQUEST.get("card_id", 0)
    card = get_card(int(card_id))
    if card:
        player.armies.acquire(card_id, int(number))
        player.update()
    return HttpResponseRedirect(reverse("mobile_debug_index"))


def add_hero(request):
    player_code = request.REQUEST.get("player_code")
    player = get_player_by_id_or_str(player_code)
    level = request.REQUEST.get("level", 1)
    hero_id = request.REQUEST.get("hero_id", 0)
    star = request.REQUEST.get("star",0)
    warrior = get_warrior(int(hero_id))
    playerhero = player.heroes.get(warrior.cardId)

    if not warrior:
        return HttpResponse("not hero %s" % hero_id)

    if not playerhero:
        playerhero = acquire_hero(player, warrior.pk, star=int(star), upgrade=warrior.hero.upgrade, level=int(level))
    else:
        playerhero.warrior_id = warrior.pk
        playerhero.upgrade = warrior.hero.upgrade
        playerhero.level = int(level) 
        playerhero.star = int(star)

    skillhero = get_heroskill(warrior.cardId)

    for i in range(0, len(skillhero.skillinfo)/3):
        skillGiId,_,upgrade = skillhero.skillinfo[i*3:(i+1)*3] 
        if upgrade < playerhero.upgrade and getattr(playerhero, "skill%sLevel" %(i+1)) < 0:
            setattr(playerhero, "skill%sLevel" %(i+1), 0)
        setattr(playerhero, "skill%sGid" %(i+1), skillGiId)
    
    player.update_hero(playerhero, True)
    player.update()
    return HttpResponseRedirect(reverse("mobile_debug_index"))

def delete_building(request):
    player_code = request.REQUEST.get("player_code")
    player = get_player_by_id_or_str(player_code)
    building_id = request.REQUEST.get("building_id", 0)
    playerbuildings = player.buildings.all().values()
    for playerbuilding in playerbuildings:
        if playerbuilding.building_id == int(building_id):
            player.buildings.delete(playerbuilding.pk)
            break
    player.update()
    
    return HttpResponseRedirect(reverse("mobile_debug_index"))

def niubility(request):
    player_code = request.REQUEST.get("player_code")
    player = get_player_by_id_or_str(player_code)

    player.gold = 999999
    player.yuanbo = 9999999
    player.wood = 9999999
    player.level = 50

    player.firstIn = 0
    player.end_tutorial()
    player.set("isOpenSiege", True)

    cur_player_buildings = player.buildings.all().keys()
    for bul in cur_player_buildings:
        player.buildings.delete(bul)
    position = [[1,0],[8,8],[17,0],[17,14],[17,11],[15,17],[12,17],[13,3],[17,7],[5,1],[0,3],[0,0],[0,11],[9,17],[13,9],[17,3]]

    i = 0
    eliminate_building = [1003001, 1003002, 1003003, 1003004, 1003005, 1003006, 1003007, 1002002, 1002003, 1001016, 1004001, 1004002, 1004003, 1004004, 1004005, 1004006, 1004007, 1004008, 1004009]
    new_buildings = get_buildings()
    for building in new_buildings:
        if i  < len(position):
            if building.pk in eliminate_building:
                continue
            acquire_building(player, building, centerX=position[i][0], centerY=position[i][1])
            i = i+1
        else:
            break
    player.setArenaOpen()
    #添加神像碎片
    buildingfragments = get_buildingfragments()
    for buildingfragment in buildingfragments:
        acquire_buildingfragment(player, buildingfragment, 1000)

    items = get_items()
    # arts = get_artifacts()
    equips = get_equips()
    souls = get_souls()
    equipsfras = get_equipfragments()
    artfras = get_artifactfragments()


    for item in items:
        acquire_item(player, item, 10000)
    for equip in equips:
        acquire_equip(player, equip, 10000)
    for eqfa in equipsfras:
        acquire_equipfragment(player, eqfa, 10000)
    # for art in arts:
    #     acquire_artifact(player, art, 10000)
    for artfa in artfras:
        acquire_artifactfragment(player, artfa, 10000)
    for soul in souls:
        acquire_soul(player, soul, 10000)
    playerheroes = player.heroes.all().keys()
    for hero in playerheroes:
        player.heroes.delete(hero)

    acquire_hero(player, 111000109, level=30, star=1, upgrade = 9)
    acquire_hero(player, 111000209, level=30, star=1, upgrade = 9)
    acquire_hero(player, 111000309, level=30, star=1, upgrade = 9)
    acquire_hero(player, 111000509, level=30, star=1, upgrade = 9)
    acquire_hero(player, 113000309, level=30, star=1, upgrade = 9)
    acquire_hero(player, 112000209, level=30, star=1, upgrade = 9)
    acquire_hero(player, 112000409, level=30, star=1, upgrade = 9)
    acquire_hero(player, 112000509, level=30, star=1, upgrade = 9)
    acquire_hero(player, 112000609, level=30, star=1, upgrade = 9)
    acquire_hero(player, 112000709, level=30, star=1, upgrade = 9)
    acquire_hero(player, 113000109, level=30, star=1, upgrade = 9)
    acquire_hero(player, 114000209, level=30, star=1, upgrade = 9)
    acquire_hero(player, 114000309, level=30, star=1, upgrade = 9)
    acquire_hero(player, 114000409, level=30, star=1, upgrade = 9)
    acquire_hero(player, 114000509, level=30, star=1, upgrade = 9)
    acquire_hero(player, 114000609, level=30, star=1, upgrade = 9)
    acquire_hero(player, 115000209, level=30, star=1, upgrade = 9)
    acquire_hero(player, 115000309, level=30, star=1, upgrade = 9)
    acquire_hero(player, 115000509, level=30, star=1, upgrade = 9)
    acquire_hero(player, 116000109, level=30, star=1, upgrade = 9)
    acquire_hero(player, 116000209, level=30, star=1, upgrade = 9)
    acquire_hero(player, 116000309, level=30, star=1, upgrade = 9)
    acquire_hero(player, 116000409, level=30, star=1, upgrade = 9)
    acquire_hero(player, 116000509, level=30, star=1, upgrade = 9)
    acquire_hero(player, 114000709, level=30, star=1, upgrade = 9)
    acquire_hero(player, 116000709, level=30, star=1, upgrade = 9)
    acquire_hero(player, 112000809, level=30, star=1, upgrade = 9)

    player.end_tutorial()


    player.update()
        
    return HttpResponseRedirect(reverse("mobile_debug_index"))

def niubility2(request):
    player_code = request.REQUEST.get("player_code")
    player = get_player_by_id_or_str(player_code)

    player.gold = 999999
    player.yuanbo = 9999999
    player.wood = 9999999
    player.level = 50

    player.firstIn = 0
    player.end_tutorial()
    player.set("isOpenSiege", True)

    cur_player_buildings = player.buildings.all().keys()
    for bul in cur_player_buildings:
        player.buildings.delete(bul)
    position = [[1,0],[8,8],[17,0],[17,14],[17,11],[15,17],[12,17],[13,3],[17,7],[5,1],[0,3],[0,0],[0,11],[9,17],[13,9],[17,3]]

    i = 0
    eliminate_building = [1003001, 1003002, 1003003, 1003004, 1003005, 1003006, 1003007, 1002002, 1002003, 1001016, 1004001, 1004002, 1004003, 1004004, 1004005, 1004006, 1004007, 1004008, 1004009]
    new_buildings = get_buildings()
    for building in new_buildings:
        if i  < len(position):
            if building.pk in eliminate_building:
                continue
            acquire_building(player, building, centerX=position[i][0], centerY=position[i][1])
            i = i+1
        else:
            break
    player.setArenaOpen()

    #添加神像碎片
    buildingfragments = get_buildingfragments()
    for buildingfragment in buildingfragments:
        acquire_buildingfragment(player, buildingfragment, 1000)

    items = get_items()
    # arts = get_artifacts()
    equips = get_equips()
    souls = get_souls()
    equipsfras = get_equipfragments()
    artfras = get_artifactfragments()


    for item in items:
        acquire_item(player, item, 10000)
    for equip in equips:
        acquire_equip(player, equip, 10000)
    for eqfa in equipsfras:
        acquire_equipfragment(player, eqfa, 10000)
    for artfa in artfras:
        acquire_artifactfragment(player, artfa, 10000)
    for soul in souls:
        acquire_soul(player, soul, 10000)

    player.end_tutorial()

    player.update()
        
    return HttpResponseRedirect(reverse("mobile_debug_index"))

def recharge(request):
    player_code = request.REQUEST.get("player_code")
    yuanbo_id = request.REQUEST.get("yuanbo_id")
    wood_id = request.REQUEST.get("wood_id")
    gold_id = request.REQUEST.get("gold_id")
    print request.POST
    player = get_player_by_id_or_str(player_code)
    if yuanbo_id:
        player.set("yuanbo" ,yuanbo_id)
    if wood_id:
        player.set("wood",wood_id)
    if gold_id:
        player.set("gold" ,gold_id)

    player.update()
    
    return HttpResponseRedirect(reverse("mobile_debug_index"))

def open_instancelevel(request):
    from module.playerinstance import api
    player_code = request.REQUEST.get("player_code")
    instancelevel_id = request.REQUEST.get("instancelevel_id")
    player = get_player_by_id_or_str(player_code)
    api._debug_open_player_instance_at_instance_id(player, int(instancelevel_id))
    player.update()
    
    return HttpResponseRedirect(reverse("mobile_debug_index"))

def open_eliteinstancelevel(request):
    from module.playerinstance import api
    player_code = request.REQUEST.get("player_code")
    instancelevel_id = request.REQUEST.get("instancelevel_id")
    player = get_player_by_id_or_str(player_code)
    api._debug_open_player_eliteinstance_at_instance_id(player, int(instancelevel_id))
    player.update()
    
    return HttpResponseRedirect(reverse("mobile_debug_index"))

def add_honor(request):


    player_code = request.REQUEST.get("player_code")

    honor_count = request.REQUEST.get("honor_count")

    score_count = request.REQUEST.get("score_count")
    player = get_player_by_id_or_str(player_code)
    if honor_count:
        player.PVP.honor = int(honor_count)
    if score_count:
        player.PVP.add_score(int(score_count))
    player.PVP.update()
    player.update()

    return HttpResponseRedirect(reverse("mobile_debug_index"))

def send_mail(request):
    from module.mail.api import send_system_mail
    from module.player.api import get_player,get_all_player
    player_code = request.REQUEST.get("player_code")
    title = request.REQUEST.get("title")
    content = request.REQUEST.get("content")
    typel = request.REQUEST.get("typel")
    count = request.REQUEST.get("count")

    players = []

    if int(player_code) == 123456:
        players = get_all_player()


    else:
        for id in player_code.strip().split(','):
            player = get_player_by_id_or_str(id)
            players.append(player)

    rewards = []
    if typel and count:

        typelst = typel.strip().split(',')
        countlst = count.strip().split(',')

        for i in range(len(typelst)):
            redict  = {}
            redict['type'] = int(typelst[i])
            redict['count'] = int(countlst[i])
            rewards.append(redict)

    contents = []
    contents.append({
        "content": content,
        "paramList": [],
    })
    

    for player in players:
        send_system_mail(player=player, sender=None, title=title, contents=contents, rewards=rewards)
    return HttpResponseRedirect(reverse("mobile_debug_index")) 
