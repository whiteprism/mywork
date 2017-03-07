# -*- coding: utf-8 -*-

from module.battlerecords.docs import PlayerBattleRecords



def send_battle_record(player, isWin,  addScore, targetPlayerId, playerScore, targetPlayerScore, playerRank,
                       targetPlayerRank, playerVip, playerIcon, targetPlayerVip, targetPlayerIcon, targetPlayerPowerRank, playerPowerRank):
    """

    """
    record = PlayerBattleRecords(
        player_id=player.pk, 
        isWin = isWin,
        addScore = addScore,
        targetPlayerId = targetPlayerId,
        playerScore = playerScore,
        targetPlayerScore = targetPlayerScore,
        playerRank = playerRank,
        targetPlayerRank = targetPlayerRank,
        playerVip = int(playerVip),
        playerIcon = playerIcon,
        targetPlayerVip = int(targetPlayerVip),
        targetPlayerIcon = targetPlayerIcon,
        targetPlayerPowerRank=targetPlayerPowerRank,
        playerPowerRank=playerPowerRank




    )
    
    record.save()



def get_records(player, lastId=0):
    """

    """
    all_records = list(PlayerBattleRecords.objects.filter(player_id=player.pk, id__gt=lastId))
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
