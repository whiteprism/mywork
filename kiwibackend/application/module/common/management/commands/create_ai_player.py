# -*- coding: utf8 -*-
from django.core.management.base import BaseCommand
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from player.api import *
from robot.models import Robot
from module.playerhero.api import *
from module.playerequip.api import *
 
class Command(BaseCommand):
    def handle(self, *args, **options):
        robots = Robot.objects.all()

        players = Player.objects.filter(id__lt=0)
        for i in players:
            i.get_playerdata()
            i.playerdata.delete()
            i.delete()

        for robot in robots:
            ai_player = create_ai_player(robot)
            print ai_player.pk
        print "############created all AI Player###############"

