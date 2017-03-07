# -*- coding: utf-8 -*-
import traceback
import sys
import logging
import datetime

class ErrorException(Exception):
    def __init__(self, player, message):
        self.player = player
        self.message = message

class AlertHandler(object):
    def __init__(self, player, response, alert_code, message):
        response.common_response.set("success", False)
        response.common_response.set("alertCode", int(alert_code))
        logging.error(
            u"\nERROR: player:%s message【%s】%s" % (player.pk, message, datetime.datetime.now())
        )

class TracebackMiddleware():
    def process_exception(self, request, exception):
        if hasattr(exception, "player"):
            logging.error(
                      u"\nERROR: player:%s message【%s】%s" % (exception.player.pk, exception.message, datetime.datetime.now())
                      )
        else:
            logging.error('######################## Exception ##################'
                      + '\n'.join(traceback.format_exception(*sys.exc_info()))
                      + '#####################################################'
                      )



