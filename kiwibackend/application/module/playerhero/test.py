# -*- coding: utf-8 -*-
from django.conf import settings
import simplejson
from playerhero.api import acquire_hero, PlayerHero

def for_player_hero_test(player):
    test_json = "%s/../doc/test.json/_create.heroes.json" % settings.ROOT_PATH
    
    fh = open(test_json, "r")
    datas = simplejson.loads(fh.read())
    fh.close()

    for data in datas:
        del data["userId"]
        warrior_id = int(data["gid"])*100
        del data["gid"]
        acquire_hero(player, warrior_id, data)
