# -*- encoding:utf8 -*-
from decorators import require_player, handle_common
from module.mail.api import get_mails, get_mail, get_mails_by_ids
from module.rewards.api import reward_send
from rewards.models import CommonReward
from module.battlerecords.api import get_records
import datetime

@handle_common
@require_player
def mailsGet(request, response):
    """
    获取邮件列表
    """
    player = request.player
    last_id = getattr(request.logic_request, "lastId", 0)
    mails = get_mails(player, last_id)

    for mail in mails:
        player.update_mail(mail)

    return response

@handle_common
@require_player
def mailRead(request, response):
    """
    读取邮件
    """
    player = request.player
    mail_id = getattr(request.logic_request, "mailId", 0)

    mail = get_mail(mail_id)
    if mail:
        #没有附件的读取玩直接删除
        #if mail.is_accept:
            #mail.delete()
            #player.delete_mail(mail.pk)
        #else:
        mail.set_is_read()
        mail.save()
        player.update_mail(mail)

    return response

@handle_common
@require_player
def mailRewardsGet(request, response):
    """
    邮件领取奖励
    """
    player = request.player
    mail_id = getattr(request.logic_request, "mailId", 0)
    status = 2  #0领取成功 1已经领取过，不能重复领取 2无法领取

    mail = get_mail(mail_id)
    if mail and mail.is_system:
        if not mail.is_accept:
        #    status = 1
        #else:
            for reward in mail.attachments:
                tmp_reward = CommonReward(reward["type"], reward["count"], 0)
                reward_send(player, tmp_reward, info=mail.title)
            status = 0

    player.delete_mail(mail.pk)
    mail.delete()
    response.logic_response.set("status", status)
    return response

@handle_common
@require_player
def mailDelete(request, response):
    """
    邮件删除
    """
    player = request.player
    mail_id = getattr(request.logic_request, "mailId", 0)
    mail = get_mail(mail_id)
    status = 0
    if not mail.is_accept:
        status = 1

    if status == 0:
        player.delete_mail(mail.pk)
        mail.delete()
    else:
        player.update_mail(mail)

    response.logic_response.set("status", status)
    return response

@handle_common
@require_player
def mailsDelete(request, response):
    """
    邮件一键删除
    """
    player = request.player
    mail_ids = getattr(request.logic_request, "mailIds", 0)

    mails = get_mails_by_ids(mail_ids)
    for mail in mails:
        if not mail.is_accept:
            continue
        mail.delete()
        player.delete_mail(mail.pk)
    return response

@handle_common
@require_player
def recordsGet(request, response):
    """
    获取战报
    """
    player = request.player
    category = getattr(request.logic_request, "category", 0) # 1 竞技场 2 攻城战
    records = get_records(player, category)
    # 清理战报 只留10条
    if len(records) > 10:
        for i in range(len(records)-1, 9, -1):
            records[i].delete()
            records.pop(i)
    result_msg = []
    for record in records:
        if record:
            _record = record.to_dict()
            _record["time"] = (datetime.datetime.now() - record.created_at).seconds
            result_msg.append(_record)

    # 每次只取最新的十条记录
    if len(result_msg) > 10:
        result_msg = result_msg[:10]

    response.logic_response.set("record", result_msg)
    return response



