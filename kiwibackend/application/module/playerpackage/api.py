# -*- coding: utf-8 -*-
from playerpackage.docs import PlayerPackage
import datetime
from django.conf import settings

def get_playerpackage(player, package_name):

    try:
        playerpackage = PlayerPackage.objects.get(package_name=package_name, player_id=player.pk)
    except:
        playerpackage = None

    return playerpackage

def use_package_code(player, package_code):
    playerpackage = PlayerPackage(package_name=package_code.package.name, player_id=player.pk, package_code=package_code.pk)
    playerpackage.save()
    package_code.is_use = True
    package_code.use_serverid = settings.SERVERID
    package_code.use_playerid = player.pk
    package_code.used_at = datetime.datetime.now()
    package_code.save()

    
