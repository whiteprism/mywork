# -*- encoding:utf8 -*-
#for test import 
from django.conf import settings
from decorators import require_player, handle_common
from module.package.api import get_package, get_package_code
from module.playerpackage.api import get_playerpackage, use_package_code
from module.mail.api import send_system_mail

@handle_common
@require_player
def packageUse(request, response):
    """
    礼包使用
    status: 1 成功；2 兑换码不存在；3 兑换码已使用；4 兑换码过期；5 兑换码无法在该渠道使用；6 兑换码无法在此服使用；7 该礼包已兑换
    """
    player = request.player
    package_code_id = getattr(request.logic_request, "packageCode", "").upper()
    package_code = get_package_code(package_code_id)

    status = 1
    if not package_code:
        status = 2
    elif package_code.is_use:
        status = 3
    elif package_code.is_expired:
        status = 4
    elif not package_code.check_channel(player.channel):
        status = 5
    elif not package_code.check_server(settings.SERVERID):
        status = 6
    else:
        playerpackage = get_playerpackage(player, package_code.package.name)

        if playerpackage and playerpackage.package_code:
            status = 7
        else:
            use_package_code(player, package_code)
            rewards = package_code.package.rewards
            rewards_dict = []
            for _reward in rewards:
                rewards_dict.append({
                    "type":_reward.type,
                    "count":_reward.count
                    })
            contents = []
            contents.append({
                "content": package_code.package.gift_body,
                "paramList": [],
            })
   
            send_system_mail(player=player, sender=None, title=package_code.package.gift_title, contents=contents, rewards=rewards_dict)
    response.logic_response.set("status", status)

    return response


@handle_common
@require_player
def testPayInterface(request, response):
    """
    """
    player = request.player
    receiptData = getattr(request.logic_request, "receiptData", "")


    if not receiptData:
        response.logic_response.set("status", 0)
        return response
    else:
        response.logic_response.set("status", 1)

    return response
