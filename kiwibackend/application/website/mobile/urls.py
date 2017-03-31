# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import *
from django.conf import settings
from mobile.views import *
urlpatterns = patterns('',
    # Example:
    # (r'^something/', include('application.foo.urls')),
)
urlpatterns += patterns('mobile.views.gateway',
     url(r'^gateway/$', "index"),
)
urlpatterns += patterns('mobile.views.baidu',
     url(r'^baidu/purchase/callback/$', "purchase_callback"),
)

if settings.LOCAL_DEBUG:
    urlpatterns += patterns('mobile.views.xls',
        url(r'^xls/$', "index", name="xls_index"),
        url(r'^xls/upload/$', "upload", name="xls_upload"),
        url(r'^xls/make/$', "make_json", name="xls_make_json"),
        url(r'^xls/load/$', "load_json", name="xls_load_json"),
        url(r'^xls/reload/$', "reload_server", name="xls_reload_server"),
    )

    urlpatterns += patterns('mobile.views.multilanguage',
        url(r'^dyy/$', "index", name="multilanguage"),
        url(r'^dyy/mix/$', "mix_txt_and_xls", name="multilanguage_going"),
    )
    urlpatterns += patterns('mobile.views.debug',
        url(r'^debug/$', "index", name="mobile_debug_index"),
        url(r'^test/$', "test", name="mobile_debug_index"),
        url(r'^powersp/add/$', "add_power_and_sp", name="mobile_debug_add_power_and_sp"),
        url(r'^recharge/$', "recharge", name="mobile_debug_recharge"),
        url(r'^level/xp/set/$', "set_level_and_xp", name="mobile_debug_set_level_and_xp"),
        url(r'^vip/set/$', "set_vip", name="mobile_debug_set_vip"),
        url(r'^tutorial/set/$', "set_tutorial", name="mobile_debug_set_tutorial"),
        url(r'^item/add/$', "add_item", name="mobile_debug_add_item"),
        url(r'^soul/add/$', "add_soul", name="mobile_debug_add_soul"),
        url(r'^equip/add/$', "add_equip", name="mobile_debug_add_equip"),
        url(r'^equipfragment/add/$', "add_equipfragment", name="mobile_debug_add_equipfragment"),
        url(r'^artifact/add/$', "add_artifact", name="mobile_debug_add_artifact"),
        url(r'^hero/add/$', "add_hero", name="mobile_debug_add_hero"),
        url(r'^warrior/add/$', "add_warrior", name="mobile_debug_add_warrior"),
        url(r'^building/delete/$', "delete_building", name="mobile_debug_delete_building"),
        url(r'^niubility/$', "niubility", name="mobile_debug_niubility"),
        url(r'^niubility2/$', "niubility2", name="mobile_debug_niubility2"),
        url(r'^instancelevel/open/$', "open_instancelevel", name="mobile_debug_open_instancelevel"),
        url(r'^eliteinstancelevel/open/$', "open_eliteinstancelevel", name="mobile_debug_open_eliteinstancelevel"),
        #url(r'^gem/add/$', "add_gem", name="mobile_debug_add_gem"),
        #url(r'^gemfragment/add/$', "add_gemfragment", name="mobile_debug_add_gemfragment"),
        url(r'^mail/send/$', "send_mail", name="mobile_debug_send_mail"),
        url(r'^honorandscore/add/$', "add_honor", name="mobile_debug_add_honor"),

        )

    urlpatterns += patterns('mobile.views.gmapi.player',
        url(r'^gmapi/player/query/$', "query_player", name="mobile_gm_player_query_player"),
        url(r'^gmapi/player/ban/$', "ban_player", name="mobile_gm_player_ban_player"),
        url(r'^gmapi/player/gag/$', "gag_player", name="mobile_gm_player_gag_player"),
    )

    urlpatterns += patterns('mobile.views.gmapi.mail',
        url(r'^gmapi/mail/sends/$', "send_mail", name="mobile_gm_mail_send_mail"),
        url(r'^gmapi/mail/query/$', "query_player_mails", name="mobile_gm_mail_query_mail"),
    )

    urlpatterns += patterns('mobile.views.gmapi.order',
        url(r'^gmapi/order/time/$', "query_orders_by_time", name="mobile_gm_order_query_by_time"),
        url(r'^gmapi/order/player/$', "query_orders_by_playerid", name="mobile_gm_order_query_by_player"),
        url(r'^gmapi/order/orderid/$', "query_orders_by_orderid", name="mobile_gm_order_query_by_orderid"),
        url(r'^gmapi/order/plat/orderid/$', "query_orders_by_plat_orderid", name="mobile_gm_order_query_by_plat_orderid"),
        url(r'^gmapi/order/rank/$', "query_rank_by_price"),
    )

    urlpatterns += patterns('mobile.views.gmapi.item',
        url(r'^gmapi/item/query/$', "query_player_items", name="mobile_gm_item_query"),
    )

    urlpatterns += patterns('mobile.views.gmapi.equip',
        url(r'^gmapi/equip/query/$', "query_player_equip", name="mobile_gm_equip_query"),
    )

    urlpatterns += patterns('mobile.views.gmapi.equipfragment',
        url(r'^gmapi/equipfragment/query/$', "query_player_equip_fragment", name="mobile_gm_equip_fragment_query"),
    )

    urlpatterns += patterns('mobile.views.gmapi.artifact',
        url(r'^gmapi/artifact/query/$', "query_player_artifact", name="mobile_gm_artifact_query"),
    )

    urlpatterns += patterns('mobile.views.gmapi.artifactfragment',
        url(r'^gmapi/artifactfragment/query/$', "query_player_artifact_fragment", name="mobile_gm_artifact_fragment_query"),
    )

    urlpatterns += patterns('mobile.views.gmapi.hero',
        url(r'^gmapi/hero/query/$', "query_player_hero", name="mobile_gm_hero_query"),
    )

    urlpatterns += patterns('mobile.views.gmapi.soul',
        url(r'^gmapi/soul/query/$', "query_player_soul", name="mobile_gm_soul_query"),
    )

    urlpatterns += patterns('mobile.views.gmapi.building',
        url(r'^gmapi/building/query/$', "query_player_building", name="mobile_gm_building_query"),
        url(r'^gmapi/buildingfragment/query/$', "query_player_buildingfragment", name="mobile_gm_buildingfragment_query"),
        url(r'^gmapi/buildingplant/query/$', "query_player_plant", name="mobile_gm_buildingplant_query"),
    )

    urlpatterns += patterns('mobile.views.gmapi.instance',
        url(r'^gmapi/instance/race/$', "query_player_raceinstance", name="mobile_gm_instance_race"),
        url(r'^gmapi/instance/elementtower/$', "query_player_elementtower", name="mobile_gm_instance_elementtower"),
    )

    urlpatterns += patterns('mobile.views.gmapi.send',
        url(r'^gmapi/send/send/$', "send_item"),
        url(r'^gmapi/send/delete/$', "delete_item"),
    )
