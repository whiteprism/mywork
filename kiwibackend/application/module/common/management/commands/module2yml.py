# -*- coding: utf8 -*-
from django.core.management.base import BaseCommand
from django.db import models
from optparse import make_option
from django.conf import settings
from django.db import models
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class Command(BaseCommand):
    option_list = BaseCommand.option_list + ( 
        make_option('--m',
            action='store',
            dest='module',
            default=False,
            help='the module name'),
       ) + (        
        make_option('--c',
            action='store',
            dest='class',
            default=False,
            help='the module class'),
        )  
    def handle(self, *args, **options):
        module_name = options.get("module")
        class_name = options.get("class")

        module = __import__(module_name)

        Cls = getattr(module.models, class_name)

        test_cls = Cls()
        if not isinstance(test_cls, models.Model):
            return 
        
        model_name = Cls.__module__.split(".")[0]
        class_name = Cls.__name__.lower()
        targetObj = Cls()

        if hasattr(Cls, "SHEET_NAME"):
            sheet_name = Cls.SHEET_NAME
        else: 
            sheet_name = class_name

        yaml_str = u"""
table:
  out-type: json
  sheet: %s
  row: 3
  model: %s.%s
  columns:
""" % (sheet_name, model_name, class_name)

        for f in targetObj._meta.fields:
            name = f.name

            if name == "id" and isinstance(f, models.IntegerField):
                continue
            #if name in TargetObj.out_yaml():
            #    continue
            if name.endswith("_str"):
                column = name[0:-4]
            elif name.endswith("_float"):
                column = name[0:-6]
            elif name.endswith("_int"):
                column = name[0:-4]
            else:
                if name =="id":
                    column = "ID"
                else:
                    column = name

            default = f.get_default()
            defaultValue = ""
            if isinstance(f, models.CharField):
                objType = "char"
                if default != None:
                    defaultValue = u"\"%s\"" % str(default)
            elif isinstance(f, models.IntegerField) or isinstance(f, models.BooleanField) or isinstance(f, models.fields.related.ForeignKey):
                objType = "int"
                if default != None:
                    defaultValue = int(default)
            elif isinstance(f, models.FloatField):
                objType = "float"
                if default != None:
                    defaultValue = float(default)
            elif isinstance(f, models.DateTimeField):
                objType = "char"
                if default != None:
                    defaultValue = u"\"%s\"" % str(default)
            else:
                continue
            

            default = f.get_default()

            yaml_str += u"    - name: %s\n      column: %s\n      type: %s\n" % (name, column, objType)
            if default != None:
                yaml_str += u"      default: %s\n" % defaultValue

            yaml_str += u"\n"

        #fh = open(u"%s/../data/yaml/%s.yml" % (settings.ROOT_PATH, class_name), "w")
        #fh.write(yaml_str)
        #fh.close()
        print yaml_str
