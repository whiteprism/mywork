# -*- coding: utf-8 -*-
from submodule.tokyotyrant import tt_operator
from module.player.models import Player
import datetime

def get_login_bonus_url(player):
    '''
    ログインボーナス
    '''
    assert isinstance(player, Player), "player must be Player instance."

    #本日の日付
    d = datetime.datetime.today()
    d_day = '%s-%s-%s' % (d.year, d.month, d.day)

    #本日、もらったかどうか
    login_bonus_days = get_login_bonus_days(player.id)

    #見つけられないなら
    if login_bonus_days.find(d_day) == -1:
        login_bonus_url = True
    else:
        login_bonus_url = False

    return login_bonus_url
        
def get_login_bonus_days(player_id):
    """ログインボーナス日付を返す"""
    if tt_operator:
        return tt_operator.get('Player::LoginBonusDays::'+str(player_id), '')
    else:
        return ''

def set_login_bonus_days(player_id, login_bonus_day):
    """ ログインボーナスをセットする """
    if tt_operator:
        days = get_login_bonus_days(player_id)
        if days == '':
            days = login_bonus_day
        else:
            days = days + ',' + login_bonus_day
        tt_operator.set('Player::LoginBonusDays::'+str(player_id), days)
