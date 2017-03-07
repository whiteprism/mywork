# -*- coding: utf8 -*-
from django.core.management.base import BaseCommand
from django.db import models
from optparse import make_option
from django.conf import settings
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from module.playerPVP.api import send_daily_pvp_rewards 

class Command(BaseCommand):
    def handle(self, *args, **options):
        send_daily_pvp_rewards()

