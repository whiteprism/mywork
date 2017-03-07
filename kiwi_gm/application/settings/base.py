# -*- coding: utf-8 -*-
DEBUG = False
ADMINS = (
    ('zhangquanming', 'quanming.zhang@fanyoy.com'),
)

MANAGERS = ADMINS

SITE_ID = 1
USE_I18N = True
USE_L10N = True

ADMIN_MEDIA_PREFIX = ''
STATIC_URL = "/static/"
SECRET_KEY = '(row!jh98s$2^l_nh7!)=user^j^l1a=a43zqb^w73+2ul'

GRAPPELLI_ADMIN_TITLE = 'KIWI GM'#更改grappellie的登入title

import os
ROOT_PATH = os.path.join(os.path.dirname(__file__),'..')
# print os.path.dirname(__file__)
# print ROOT_PATH
import sys
sys.path.append(ROOT_PATH+'/../')
sys.path.append(ROOT_PATH+'/website/')
sys.path.append(ROOT_PATH+'/module/')

# sys.path.append(os.path.abspath('../../'))
# sys.path.append(os.path.abspath('../'))
# sys.path.append(os.path.abspath('../website'))
# sys.path.append(os.path.abspath('../module'))


# print sys.path
ROOT_URLCONF = 'application.urls'

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'opensocial',
    'gameconfig',
    'common',
    'feedback',
    'server',
)
#CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'opensocial.middleware.TracebackMiddleware',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'TIMEOUT' : 3600,
    },
}
MEDIA_ROOT = "%s/../static" % (ROOT_PATH)
WHITE_LIST  = []


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
)
TEMPLATE_DIRS = (
   ROOT_PATH + '/website/templates/',
)

from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'common.context_processors.contexts',
)
