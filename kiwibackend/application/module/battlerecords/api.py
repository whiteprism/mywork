# -*- coding: utf-8 -*-

from module.battlerecords.docs import PlayerBattleRecords



def send_battle_record(player, targetPlayer, isWin, category, addScore=0, playerHeroes={}, targetHeroes={}, playerWallSoldiers=[], targetWallSoldiers=[], resource={}):
    """
        保存战报
    """
    record = PlayerBattleRecords(
        player_id = player.pk,
        isWin = isWin,
        category = category,
        addScore = addScore,
        playerPvpRank = player.pvpSimple_dict(),
        targetPvpRank = targetPlayer.pvpSimple_dict(),
        playerPowerRank = player.powerRank,
        targetPowerRank  = targetPlayer.powerRank,
        playerHeroes = playerHeroes,
        targetHeroes = targetHeroes,
        playerSimple = player.userSimple_dict(),
        targetSimple = targetPlayer.userSimple_dict(),
        playerWallSoldiers = playerWallSoldiers,
        targetWallSoldiers = targetWallSoldiers,
        resource = resource
    )

    record.save()

def get_records(player, category, lastId=0):
    """

    """
    all_records = list(PlayerBattleRecords.objects.filter(player_id=player.pk, id__gt=lastId, category=category))
    records = []
    for record in all_records:

        records.append(record)
    return records


def get_record(mail_id):
    """

    """
    try:
        record = PlayerBattleRecords.objects.get(pk=mail_id)
    except:
        record = None

    return record
