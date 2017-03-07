# -*- coding: utf-8 -*-
from django.contrib import admin
from gameconfig.models import *

class GameModelAdmin(admin.ModelAdmin):
    list_display = ('sort','name','secret_level')

class GameFuncAdmin(admin.ModelAdmin):
    pass

class GameAuthAdmin(admin.ModelAdmin):
    pass


admin.site.register(GameModel, GameModelAdmin)
admin.site.register(GameFunc, GameFuncAdmin)
admin.site.register(GameAuth, GameAuthAdmin)
