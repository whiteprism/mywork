# /usr/bin/env python
# -*- coding: utf-8 -* 

from django.core.cache import get_cache

def decorate_active_player(view_func):
    @wraps(view_func)
    def decorate(request, *args, **kwds):
        player = request.player
        if player and player.is_end_tutorial():
            _add_active_player(player)
        return view_func(request, *args, **kwds)
    return decorate
