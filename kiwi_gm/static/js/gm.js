/*function gmPost(url, data, func){
    $.post(url, data, function(html){
        var patt1 = new RegExp("/static/grappelli/js/grappelli.min.js");

        if (patt1.test(html)){
            location.reload();
            return;
        }else {
            return func(html);
        }

    });
}*/

function gmPost(url, data, func){
    $.post(url, data, function(html){
        if (html.indexOf("/static/grappelli/js/grappelli.min.js") > 0){
            location.reload();
            return ;
        }else {
            return func(html);
        }

    });
}

function sendItem(){
    if ($.trim($("#inputUserID").val()).length == 0){
        alert("请输入用户ID");
    }
    else if($.trim($("#inputItemType").val()).length == 0){
        alert("请输入物品ID！");
    }
    else if($.trim($("#inputCount").val()).length == 0){
        alert("请输入物品数量！");
    }
    else {
        gmPost("/send/send_item/", $("#formid").serialize(), function(html){
            $(".game-container").html(html);
        });
    }
}

function deleteItem(){
    if ($.trim($("#inputUserID").val()).length == 0){
        alert("请输入用户ID");
    }
    else if($.trim($("#inputItemType").val()).length == 0){
        alert("请输入物品ID！");
    }
    else if($.trim($("#inputCount").val()).length == 0){
        alert("请输入物品数量！");
    }
    else {
        gmPost("/send/delete_item/", $("#formid").serialize(), function(html){
        $(".game-container").html(html);
        });
    }
}

function getPropertyInfo(form){
    if ($.trim($("#inputUserID").val()).length == 0){
        alert("请输入用户ID");
    }
    else if($.trim($("input:radio[name='type']:checked").val()).length == 0){
        alert("请选择查询类型！");
    }
    else {
        gmPost("/item/query/", $(form).serialize(), function(html){
        $("#get-item-table").html(html);
        });
    }
}

function getMail(form){
    if ($.trim($("#inputUserID").val()).length == 0){
        alert("请输入用户ID");
    }
    else {
        gmPost("/mail/get/", $(form).serialize(), function(html){
        $("#get-mail-table").html(html);
        });
    }
}

function sendMail(form){
    if ($.trim($("#inputUserIDs").val()).length == 0){
        alert("请输入用户ID");
    }
    else if($.trim($("#inputMailTitle").val()).length == 0){
        alert("请输入邮件标题！");
    }
    else {
        gmPost("/mail/send/", $(form).serialize(), function(html){
        $("#send-mail-table").html(html);
        });
    }
}

function getOrderByUser(form){
    if ($.trim($("#inputUserID").val()).length == 0){
        alert("请输入用户ID");
    }
    else {
        gmPost("/order/by_user/", $(form).serialize(), function(html){
        $("#order-search-table-by-user").html(html);
        });
    }
}

function getOrderByOrderID(form){
    if ($.trim($("#inputOrderID").val()).length == 0){
        alert("请输入订单ID");
    }
    else {
        gmPost("/order/by_order/", $(form).serialize(), function(html){
        $("#order-search-table-by-orderid").html(html);
        });
    }
}

function getOrderByPlat(form){
    if ($.trim($("#inputPlatOrderID").val()).length == 0){
        alert("请输入平台ID");
    }
    else {
        gmPost("/order/by_plat/", $(form).serialize(), function(html){
        $("#order-search-table-by-plat").html(html);
        });
    }
}

function getOrderByTime(form){
    if ($.trim($("#inputStartTime").val()).length == 0 || $.trim($("#inputEndTime").val()).length == 0){
        alert("请选择查询时间");
    }
    else {
        gmPost("/order/by_time/", $(form).serialize(), function(html){
        $("#order-search-table-by-time").html(html);
        });
    }
}

function checkRechargeRank(form){
    if ($.trim($("#inputStartTime2").val()).length == 0 || $.trim($("#inputEndTime2").val()).length == 0){
        alert("请选择查询时间");
    }
    else {
        gmPost("/order/rank/", $(form).serialize(), function(html){
        $("#order-rank-table").html(html);
        });
    }
}

function change_server(){
    document.cookie = "sid=" + $("#forserver").val();
}

function sync_server(){
    gmPost("/server/sync/",{},function(resdata){
        $(".game-container").html(resdata);
    });
}

function switch_model(url, modelID){
    gmPost("/model/", {id:modelID}, function(html){
        $(".game-container").html(html);
    });
    $(".model-nav-list > li").removeClass("active");
    $("." + "model-" + modelID).addClass("active");
}

function userGetInfo(form){
    if ($.trim($("#inputUserID").val()).length == 0 && $.trim($("#inputUserNick").val()).length == 0){
        alert("用户ID不能为空");
    }
    else {
        gmPost("/user/search/", $(form).serialize(), function(html){
        $("#user-search-table").html(html);
        });
    }
}

function actionGetInfo(form){
/*    var chestr = "";
    for(i=1;i<18;i++)
    {
        var elements = document.getElementsByName(String(i));
        for(j=0;j<elements.length;j++)
        {
            if(elements[j].checked == true)
            {
                chestr += elements[j].value;
            }
        }
    }*/
    if($.trim($("#inputUserID").val()).length == 0){
    alert("用户ID不能为空");
    }
    else if($.trim($("#inputStartTime").val()).length == 0 || $.trim($("#inputEndTime").val()).length == 0){
        alert("请选择查询起始时间！");
    }
    else{
        gmPost("/action/get/", $(form).serialize(), function(html){
        $("#action-search-table").html(html);
        });
    }
}

function serverGetInfo(form){
    gmPost("/server/search/", $(form).serialize(), function(html){
    $("#server-search-table").html(html);
    });
}

function serverNotimeGetInfo(form){
    gmPost("/server/search_notime/", $(form).serialize(), function(html){
    $("#server-search-notime-table").html(html);
    });
}

function rechargeGetInfo(form){
    gmPost("/recharge/search_recharge/", $(form).serialize(), function(html){
    $("#recharge-search-table").html(html);
    });
}

function sendMessage(form){
    gmPost("/sendmessage/send/", $(form).serialize(), function(html){
    $("#recharge-search-table").html(html);
    });
}

function elementGetInfo(form){
    gmPost("/element/search_element/", $(form).serialize(), function(html){
    $("#server-search-notime-table").html(html);
    });
}

function deleteelement(form){
    gmPost("/element/delete_element/", $(form).serialize(), function(html){
    $("#delete-element-search-table").html(html);
    });
}

function send_welfare(form){
    gmPost("/welfare/send_welfare/", $(form).serialize(), function(html){
    $("#welfare-send-table").html(html);
    });
}

function orderGetInfo(form){
    gmPost("/order/search_order/", $(form).serialize(), function(html){
    $("#order-search-table").html(html);
    });
}

function orderFake(form){
    gmPost("/order/fake_order/", $(form).serialize(), function(html){
    $("#order-fake-result").html(html);
    });
}

function addOrder(serverid,orderid){
    gmPost("/order/add_order/", {server_id:serverid,order_id:orderid}, function(html){
       $("#user-search-table").html(html);
    });
}

function userBan(userID,serverID){
    gmPost("/user/ban/", {userID:userID,serverID:serverID}, function(html){
    $("#user-search-table").html(html);
    });
}

function userGag(userID,serverID){
    gmPost("/user/gag/", {userID:userID,serverID:serverID}, function(html){
       $("#user-search-table").html(html);
    });
}

function responseEmail(email,message){
    gmPost("/feedback/response/",{email:email,message:message},function(data){
        $(".game-container").html(data);
    })
}

function sendEmail(form){
    gmPost("/feedback/send_email/", $(form).serialize(), function(data){
    $("#").html(data);
    });
}
