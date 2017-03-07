# -*- coding: utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from optparse import make_option
from django.core.management.base import BaseCommand
from guild.api import guild_siege_join

class Command(BaseCommand):
    option_list = BaseCommand.option_list + ( 
        make_option('--p',
            action='store',
            default=False,
            help='the module name'),
       )        
    def handle(self, *args, **options):
        guild_siege_join()



