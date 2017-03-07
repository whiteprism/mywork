# /usr/bin/env python
# -*- coding: utf-8 -* 

from functools import wraps

from django.core.cache import get_cache

cache = get_cache('master')

ACTIVE_PLAYER_LEN = 500

def active_player_key(level):
    return 'active_player_%d' % level

def decorate_active_player(view_func):
    @wraps(view_func)
    def decorate(request, *args, **kwds):
        player = request.player
        if player and player.is_end_tutorial():
            _add_active_player(player)
        return view_func(request, *args, **kwds)
    return decorate

def _add_active_player(player):
    active_player = cache.get(active_player_key(player.level), [])
    if player.pk in active_player:
        return
    if len(active_player) >= ACTIVE_PLAYER_LEN:
        active_player = active_player[len(active_player)-ACTIVE_PLAYER_LEN+1:]
    active_player.append(player.pk)
    cache.set(active_player_key(player.level), active_player)

def get_active_player(level, float_level=10):
    active_player_id_list = []
    for i in xrange((level-float_level) if (level>float_level) else 3, level+float_level):
        active_player_id_list += cache.get(active_player_key(i), [])
    return active_player_id_list
