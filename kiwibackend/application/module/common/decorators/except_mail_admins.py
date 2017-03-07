# -*- coding: utf-8 -*-
import sys
import traceback
from functools import wraps

from django.conf import settings
from django.core.mail import mail_admins
from django.utils.encoding import smart_str, smart_unicode

def except_mail_admins(method):
    @wraps(method)
    def decorate(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except Exception, e:
            _mail_admins_exception(e, *args, **kwargs)
    return decorate

#ERROR_MAIL_SUBJECT_TEMPLATE = u"""%(SANDBOX_SIGN)s%(SYSTEM_NAME)s ActionLog Write Error. %(EXCEPTION_TYPE)s"""
ERROR_MAIL_SUBJECT_TEMPLATE = """%(SANDBOX_SIGN)s%(SYSTEM_NAME)s Except-Mail-Admins Decorator. %(EXCEPTION_TYPE)s"""

ERROR_MAIL_MESSAGE_TEMPLATE = u"""\
system_name:
    %(SANDBOX_SIGN)s%(SYSTEM_NAME)s

hostname:
    %(HOSTNAME)s

exception_type:
    %(EXCEPTION_TYPE)s

exception_message:
    %(EXCEPTION_MESSAGE)s

args:
    %(ARGS)s

kwargs:
    %(KWARGS)s

----------------------------------------
%(TRACEBACK_LOG)s
----------------------------------------
"""

def _mail_admins_exception(exception, *args, **kwargs):
    values = {
        'SANDBOX_SIGN' : _get_sandbox_sign(),
        'SYSTEM_NAME' : _get_system_name(),
        'HOSTNAME' : _get_hostname(),
        'EXCEPTION_TYPE' : exception.__class__.__name__,
        'EXCEPTION_MESSAGE': smart_unicode(exception.message),
        'ARGS' : repr(args),
        'KWARGS' : repr(kwargs),
        'TRACEBACK_LOG' : smart_unicode('\n'.join(traceback.format_exception(*sys.exc_info()))),
    }
    try:
        subject = ERROR_MAIL_SUBJECT_TEMPLATE % values
    except UnicodeDecodeError:
        subject = u'subject unavalable(UnicodeDecodeError) %r' % values
    try:
        message = ERROR_MAIL_MESSAGE_TEMPLATE % values
    except UnicodeDecodeError:
        message = u'message unavalable(UnicodeDecodeError)\n%r' % values
    
    if getattr(settings,'OPENSOCIAL_DEBUG', False):
        mail_admins(subject, message, fail_silently=True)
    else:
        mail_admins(subject, message)


def _get_sandbox_sign():
    if getattr(settings, 'OPENSOCIAL_SANDBOX', False):
        return u'[SANDBOX] '
    else:
        return u''


def _get_hostname():
    try:
        import socket
        return unicode(socket.gethostbyaddr(socket.gethostname())[0])
    except:
        return u''


def _get_system_name():
    """
    取得系统名
    """
    try:
        system_name = settings.DATABASES['default']['NAME']
    except:
        system_name = "SystemName unavailable."
    return system_name

