# -*- coding: utf-8 -*-
from django.conf import settings

def contexts(request):
    return { 'request' : request,
             'settings': settings,
             }

