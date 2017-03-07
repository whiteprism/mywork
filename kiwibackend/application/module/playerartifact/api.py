# -*- coding: utf-8 -*-
from module.utils import is_digits
from playerartifact.docs import PlayerArtifact, PlayerArtifactFragment
from artifact.models import Artifact, ArtifactFragment
from artifact.api import get_artifact
from module.common.actionlog import ActionLogWriter
import random
from django.conf import settings

def acquire_artifact(player, artifact_or_artifact_id, info="", **argvs):
    ''' 
    获取圣物
    '''
    if isinstance(artifact_or_artifact_id, Artifact):
        artifact_id = artifact_or_artifact_id.pk
    elif is_digits(int(artifact_or_artifact_id)):
        artifact_id = int(artifact_or_artifact_id)

    playerartifact = player.artifacts.create(artifact_id = artifact_id, **argvs)
    ActionLogWriter.artifact_acquire(player, playerartifact.pk, artifact_id, info)
    artifact = get_artifact(artifact_id)
    playerartifact.get_random_skill(artifact)
    player.update_artifact(playerartifact, True)
    return playerartifact

def get_playerhero_artifacts(player, playerhero):
    """
    获取playerhero的圣物
    """
    return get_playerheroes_artifacts(player, [playerhero])

def get_playerheroes_artifacts(player, playerheroes):
    """
    获取playerheroies的圣物
    """
    playerartifacts = []
    for playerhero in playerheroes:
        attack_playerartifact_id = playerhero.get_equip(5) 
        defense_playerartifact_id = playerhero.get_equip(6) 
        if attack_playerartifact_id:
            playerartifacts.append(player.artifacts.get(attack_playerartifact_id))
        if defense_playerartifact_id:
            playerartifacts.append(player.artifacts.get(defense_playerartifact_id))
    return playerartifacts

def acquire_artifactfragment(player, fragment_or_fragment_id, number=1, info="", **argvs):
    ''' 
    获取圣物碎片
    '''
    if isinstance(fragment_or_fragment_id, ArtifactFragment):
        fragment_id = fragment_or_fragment_id.pk
    elif is_digits(int(fragment_or_fragment_id)):
        fragment_id = int(fragment_or_fragment_id)

    # playerfragment = player.get_artifactfragment(fragment_id) 
    # playerfragment.add(number, info=info)
    # playerfragment.save()
    # player.update_artifactfragment(playerfragment)
    # return playerfragment
    _, playerartifactfragment = player.artifactfragments.get_or_create(fragment_id, obj_id=fragment_id, **argvs)
    playerartifactfragment.add(number, info)
    player.update_artifactfragment(playerartifactfragment, True)
    
    return playerartifactfragment

# def get_playerartifactfragments(player):
#     return list(PlayerArtifactFragment.objects.filter(player_id = player.pk))

# def get_playerartifactfragment_by_fragment(player, fragment_id):
#     try:
#         data = PlayerArtifactFragment.objects.get(player_id = player.pk, fragment_id = fragment_id)
#     except:
#         data = PlayerArtifactFragment(player_id = player.pk, fragment_id = fragment_id, level=player.level)
#         data.is_new = True
#     return data

# def get_playerartifactfragments_by_artifact(player, artifact_or_artifact_id):
#     """
#     根据圣物获取玩家圣物碎片
#     """
#     if isinstance(artifact_or_artifact_id, Artifact):
#         artifact = artifact_or_artifact_id
#     elif is_digits(int(artifact_or_artifact_id)):
#         artifact = get_artifact(artifact_or_artifact_id)

#     # fragments = artifact.fragment_ids

#     playerfragments = PlayerArtifactFragment.objects.filter(player_id=player.pk, fragment_id__in=fragments)

#     return playerfragments

# def get_player_list_by_fragment_and_level(player, fragment_id, is_all=True):
#     """
#     根据等级过滤用户
#     """
#     from module.player.docs import Player
#     from module.player.api import get_player

#     playerAId = None
#     playerBId = None
#     playerCId = None
#     playerDId = None
#     playerEId = None

#     oppIds = []

#     if is_all:
#         playerInfos = list(PlayerArtifactFragment.objects.filter(
#             level__gt = player.level - 4,
#             level__lt = player.level + 4,
#             fragment_id = fragment_id, 
#             count__gte = 1,
#             serverid__in = settings.ALL_SERVERS
#         ).only("player_id", "level"))

#         playerInfos=list(playerInfos)
#         random.shuffle(playerInfos)

#         #免战

#         for _playerInfo in playerInfos:
#             if playerAId and playerBId and playerCId:
#                 break
            
#             #免战期
#             targetPlayer = get_player(_playerInfo.player_id)
#             if targetPlayer.in_waravoid:
#                 continue

#             if not playerAId:
#                 if _playerInfo.player_id != player.pk and player.level - 1 < _playerInfo.level < player.level + 4:
#                     playerAId = _playerInfo.player_id
#                     continue

#             if not playerBId:
#                 if _playerInfo.player_id != player.pk and player.level - 2 < _playerInfo.level < player.level + 2:
#                     playerBId = _playerInfo.player_id
#                     continue

#             if not playerCId:
#                 if _playerInfo.player_id != player.pk and player.level - 4 < _playerInfo.level < player.level + 1:
#                     playerCId = _playerInfo.player_id
#                     continue

#     #机器人
#     players = Player.objects.filter(
#         id__lt = 0,
#         level__gt = player.level - 4,
#         level__lt = player.level + 3,
#     )
#     players=list(players)
#     random.shuffle(players)

#     for _player in players:
#         if playerAId and playerBId and playerCId and playerDId and playerEId:
#             break

#         if not playerAId:
#             if player.level - 1 < _player.level < player.level + 4:
#                 playerAId = _player.pk
#                 continue

#         if not playerBId:
#             if player.level - 2 < _player.level < player.level + 2:
#                 playerBId = _player.pk
#                 continue

#         if not playerCId:
#             if player.level - 4 < _player.level < player.level + 1:
#                 playerCId = _player.pk
#                 continue

#         if not playerDId:
#             if player.level - 3 < _player.level < player.level + 3:
#                 playerDId = _player.pk
#                 continue

#         if not playerEId:
#             if player.level - 4 < _player.level < player.level + 1:
#                 playerEId = _player.pk
#                 continue

#     if playerAId:
#         oppIds.append(playerAId)
#     if playerBId:
#         oppIds.append(playerBId)
#     if playerCId:
#         oppIds.append(playerCId)
#     if playerDId:
#         oppIds.append(playerDId)
#     if playerEId:
#         oppIds.append(playerEId)

#     opps = list(Player.objects.filter(pk__in=oppIds))
#     return opps


