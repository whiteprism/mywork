#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import os
import sys

if __name__ == "__main__":
#当不指定--settings=settings.xsf　这种方式的时候默认就会使用这个默认值.
#    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
