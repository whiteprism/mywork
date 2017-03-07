# -*- coding: utf-8 -*-

# エラーメールを送信するスクリプト。
# from fanyoy.error_mail import send_error_mail
# send_error_mail("本文","件名") で送信できる。


import traceback
import subprocess
import datetime
import logging

from django.core.mail import send_mail
from django.conf import settings


MAIL_SUBJECT_PREFIX = u"[ERROR:%s]" % settings.SITE_DOMAIN

ENVIRONMENT_TEMPLATE = u"""

--------------------------------
[ Status ]
APP_NAME   : %(APP_NAME)s
SITE_DOMAIN: %(SITE_DOMAIN)s
Hostname   : %(HOSTNAME)s
DateTime   : %(DATETIME)s
"""

TRACEBACK_TEMPLATE = u"""\
--------------------------------
[ Traceback ]
%(TRACEBACK)s
"""



def send_error_mail(message,subject=u""):
    """
    settings.ADMINS に、エラーメールを送信する
    """
    
    message = to_unicode(message)
    subject = to_unicode(subject)
    
    message_environment = ENVIRONMENT_TEMPLATE % {
        'APP_NAME'    : settings.APP_NAME,
        'SITE_DOMAIN' : settings.SITE_DOMAIN,
        'HOSTNAME'    : get_hostname(),
        'DATETIME'    : get_datestring(),
    }
    
    message_traceback = TRACEBACK_TEMPLATE %{
        'TRACEBACK' : "\n".join(traceback.format_stack()[-3:-1]),
    }
    
    message_body = message + message_environment + message_traceback
    
    if settings.OPENSOCIAL_DEBUG:
        logging.debug("send_error_mail subject: %s" % MAIL_SUBJECT_PREFIX + subject)
        logging.debug("send_error_mail body: %s" % message_body)
        return
    
    send_mail(
        MAIL_SUBJECT_PREFIX + subject,
        message_body,
        settings.SERVER_EMAIL,
        get_admin_mail_list(),
        fail_silently=False
    )
    
    return


def get_hostname():
    try:
        hostname = subprocess.Popen(["hostname"],stdout=subprocess.PIPE).communicate()[0]
        hostname = hostname.strip()
    except:
        hostname = "Hostname error."
    return hostname

def get_datestring():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def to_unicode(s):
    if type(s) == str:
        s = s.decode('utf-8','ignore')
    return s

def get_admin_mail_list():
    mail_list = [a[1] for a in settings.ADMINS]
    return mail_list
