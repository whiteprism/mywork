# -*- coding: utf-8 -*-
from loginbonus.models import LoginBonus, LoginBonusReward

def update_loginbonus_cache():
    LoginBonus.create_cache()
    LoginBonusReward.create_cache()

def get_loginbonus(pk):
    return LoginBonus.get(pk)

