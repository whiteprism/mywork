# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from opensocial.models import OsUser, OsAccount
from common.decorators.memoized_property import memoized_property_set

def get_osaccount(channel, account):
    """
    获取账号信息
    """
    key = OsAccount.get_osKey(channel, account)
    return OsAccount.get(key)

def get_osuser(osuser_id):
    """
    获得opensocial user
    """
    return OsUser.get(osuser_id)

def create_osaccount(channel, account, password="", email="", tel=0, tel_zone=0, username="", is_binding=0):
    """
    创建opensocial user
    """
    key = int(OsUser._incrment_id())
    osuser = OsUser.create(key, id=key, channel_id=channel.pk, password=password, email=email, tel=tel, tel_zone=tel_zone, _username=username, is_binding=is_binding)

    key = OsAccount.get_osKey(channel, account)
    osaccount = OsAccount.create(key, account=account,  osuser_id=osuser.id, channel_id=channel.pk)
    memoized_property_set(osaccount, "osuser", osuser)
    return osaccount

def binding_osaccount_by_tel(channel, account, password, osuser, tel, tel_zone):
    """
    用户绑定
    """
    osuser.binding_tel(password, tel_zone, tel)
    key = OsAccount.get_osKey(channel, account)
    osaccount = OsAccount.create(key, account=account, osuser_id=osuser.id, channel_id=channel.pk)
    memoized_property_set(osaccount, "osuser", osuser)
    return osaccount

def binding_osaccount_by_email(channel, account, password, osuser, email):
    """
    用户绑定
    """
    osuser.binding_email(password, email)
    key = OsAccount.get_osKey(channel, account)
    osaccount = OsAccount.create(key, account=account, osuser_id=osuser.id, channel_id=channel.pk)
    memoized_property_set(osaccount, "osuser", osuser)
    return osaccount

def secret_osaccount_by_tel(channel, account, osuser, tel, tel_zone):
    """
    安全设定 电话
    """
    osuser.secret_tel(tel_zone, tel)
    key = OsAccount.get_osKey(channel, account)
    osaccount = OsAccount.create(key, account=account, osuser_id=osuser.id, channel_id=channel.pk)
    memoized_property_set(osaccount, "osuser", osuser)
    return osaccount

def secret_osaccount_by_email(channel, account, osuser, email):
    """
    安全设定 邮箱
    """
    osuser.secret_email(email)
    key = OsAccount.get_osKey(channel, account)
    osaccount = OsAccount.create(key, account=account, osuser_id=osuser.id, channel_id=channel.pk)
    memoized_property_set(osaccount, "osuser", osuser)
    return osaccount
