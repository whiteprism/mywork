# -*- coding: utf-8 -*-
from player.api import get_player
#from playergashapon.api import acquire_gashapon
from gashapon.api import get_gashapon

def test_acquire_gashapon(player):

    for i in range(1, 5):
#        gashapon = get_gashapon(i)
        print "#####" * 10
        print acquire_gashapon(player, gashapon)
        print "#####" * 10
