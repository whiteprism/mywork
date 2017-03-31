# -*- coding: utf-8 -*-

from module.mail.docs import PlayerMail

def has_unread_mails(player):
    """
    是否有未读邮件
    """
    return PlayerMail.objects.filter(player_id=player.pk, status=0).count()

def send_system_mail(player, sender, title, contents=[], rewards=[]):
    """
    发送系统邮件
    """
    mail = PlayerMail(
        player_id=player.pk, 
        title=title,
        category=1,
        attachments=rewards,
        contents=contents,
    )
    
    mail.save()

def get_mail(mail_id):
    """
    获取邮件
    """
    try:
        mail = PlayerMail.objects.get(pk=mail_id)
    except:
        mail = None

    return mail

def get_mails_by_ids(mail_ids):
    """
    获取邮件
    """
    return PlayerMail.objects.filter(pk__in=mail_ids)

def get_mails(player, lastId=0):
    """
    获取邮件
    """
    all_mails = list(PlayerMail.objects.filter(player_id=player.pk, id__gt=lastId))
    mails = []
    for mail in all_mails:
        if mail.is_timeout:
            mail.delete()
        else:
            mails.append(mail)
    return mails
    
def send_attack_mail(player, sender, title, contents, playback, isWin, mailType, rewards):
    """
    攻击信息
    """
    sendInfo = {
        "icon": sender.iconId,
        "name": sender.name,
    }
    mail = PlayerMail(
        player_id=player.pk, 
        playerName = player.name,
        title = title,
        contents = contents,
        category = 2,
        isWin = isWin,
        playback = playback,
        mailType = mailType,
        attachments = rewards,
        sender = sendInfo,
        # sender = sender.userSimple_dict(), # 数据冗余
    )
    mail.save()
    
def send_defense_mail(player, sender, title, contents, playback, isWin, mailType=1, rewards=[]):
    """
    防御信息
    """
    sendInfo = {
        "icon": sender.iconId,
        "name": sender.name,
    }
    mail = PlayerMail(
        player_id=player.pk, 
        playerName = player.name,
        title = title,
        contents = contents,
        category = 3,
        isWin = isWin,
        playback = playback,
        mailType = mailType,
        attachments = rewards,
        sender = sendInfo,
        # sender = sender.userSimple_dict(),
        # paramList = params
    )
    mail.save()
