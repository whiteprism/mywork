# -*- coding: utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from optparse import make_option
from django.core.management.base import BaseCommand

from module.package.api import get_package, generate_package_code
 
class Command(BaseCommand):
    option_list = BaseCommand.option_list + ( 
        make_option('--p',
            action='store',
            dest='pkg_id',
            default=False,
            help='the module name'),
       )        
    def handle(self, *args, **options):
        pkg_id = options.get("pkg_id")
    
        pkg = get_package(pkg_id)
        generate_package_code(pkg)


