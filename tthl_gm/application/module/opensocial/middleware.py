# -*- coding: utf-8 -*-
from django.db import connection
import traceback
import sys
import logging

class TracebackMiddleware():
    def process_exception(self, request, exception):
        logging.error('######################## Exception ##################'
                      + '\n'.join(traceback.format_exception(*sys.exc_info()))
                      + '#####################################################'
                      )

