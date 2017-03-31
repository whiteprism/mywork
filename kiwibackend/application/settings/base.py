# -*- coding: utf-8 -*-

# default
DEBUG = True
TEMPLATE_DEBUG = DEBUG
OPENSOCIAL_DEBUG = False

ADMINS = (
    ('guochao', 'gchsuperman@gmail.com'),
)

MANAGERS = ADMINS

SITE_ID = 1

# default
USE_I18N = True
# default
USE_L10N = True

ADMIN_MEDIA_PREFIX = '/media/'

# default
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(row!jh98s$2^l_nh7!)=93c5v7^j^l1a=a%43zqb^w73+2ul%'

import os
ROOT_PATH = os.path.join(os.path.dirname(__file__),'..')

# 优先搜索的ｕｌｒｓ的路径
ROOT_URLCONF = 'application.urls'

import sys
sys.path.append(ROOT_PATH+'/website/')
sys.path.append(ROOT_PATH+'/submodule/')
sys.path.append(ROOT_PATH+'/module/')
sys.path.append(ROOT_PATH+'/submodule/fanyoy/')
sys.path.append(ROOT_PATH+'/../')
MIDDLEWARE_CLASSES = (
    # default
    "django.middleware.common.CommonMiddleware",
    # default
    "django.contrib.sessions.middleware.SessionMiddleware",
    # default
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # default
    "django.contrib.messages.middleware.MessageMiddleware",
    # how to use this ???
    "common.middleware.TracebackMiddleware",
)

INSTALLED_APPS = (
    # default
    'django.contrib.auth',
    # default
    'django.contrib.contenttypes',
    # default
    'django.contrib.sessions',
    #  ??? how to use this ??
    'django.contrib.sites',
    # default
    'django.contrib.messages',
    # default
    'django.contrib.admin',
    # --------------------bellow is manual added -------------------------------------------
    # 'djcelery', 
    'common',
    'skill',
    'hero',
    'gashapon',
    'soul',
    'instance',
    'equip',
    'attr',
    'building',
    'levelconf',
    'item',
    'artifact',
    'task',
    'vip',
    'activity',
    'arenashop',
    'mysteryshop',
    'yuanbo',
    'experiment',
    'icon',
    'pvp',
    'tutorial',
    'robot',
    'package',
    'loginbonus',
    'offlinebonus',
    'guild',
)

def _get_hostname():
    try:
        import socket
        return socket.gethostbyaddr(socket.gethostname())[0]
    except:
        return ''
HOSTNAME = _get_hostname()
SOUTH_TESTS_MIGRATE = False
#SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# default
TIME_ZONE = 'Asia/Shanghai'
# default
LANGUAGE_CODE = 'zh-hans'
# default USE_TZ
#USE_TZ = True
ENABLE_REDIS_CACHE = True
BUNDLEURL = "http://192.168.1.2/"
STATIC_CONFS = {}
LOCAL_DEBUG = True
OPEN_PAYMENT = True

def yoyprint(message):
    pass
__builtins__["yoyprint"]  = yoyprint

# default
STATIC_URL = '/static/'
STATIC_ROOT = 'static'

TEMPLATE_DIRS = (
   ROOT_PATH + '/website/mobile/templates/',
)
KVS_BASE_NAME = "KIWI" #kiwi
ENABLE_REDIS_CACHE = False
