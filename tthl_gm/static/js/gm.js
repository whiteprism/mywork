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

function switch_model(url, modelID){
    gmPost("/model/", {id:modelID}, function(html){
    $(".game-container").html(html);
    });
    $(".model-nav-list > li").removeClass("active");
    $("." + "model-" + modelID).addClass("active");
}

function userGetInfo(form){
    if($.trim($("#inputServerID").val()).length == 0){
        alert("请输入服务器ID");
        $("#inputServerID").focus();
    }
    else if ($.trim($("#inputUserID").val()).length == 0 && $.trim($("#inputUserNick").val()).length == 0){
        alert("请输入用户ID");
        $("#inputUserID").focus();
    }
    else {
        gmPost("/action/search/", $(form).serialize(), function(html){
        $("#user-search-table").html(html);
        });
    }
}

function actionGetInfo(){
    var chestr = "";
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
    }
    if($.trim($("#playerid").val()).length == 0){
        alert("请输入用户ID");
        $("#playerid").focus();
    }
    else if(!chestr){
        alert("请选择查询动作");
    }
    else{
        gmPost("/action/search/", $("#form1").serialize(), function(html){
        $("#action-search-table").html(html);
        });
    }
}

function serverGetInfo(form){
    if($.trim($("#inputServerID").val()).length == 0){
        alert("请输入服务器ID");
        $("#inputServerID").focus();
    }
    else if($.trim($("#inputStartTime").val()).length == 0 || $.trim($("#inputEndTime").val()).length == 0){
        alert("请选择查询时间");
    }
    else{
        gmPost("/server/search/", $(form).serialize(), function(html){
        $("#server-search-table").html(html);
        });
    }
}

function serverNotimeGetInfo(form){
    if($.trim($("#inputServerID2").val()).length == 0){
        alert("请输入服务器ID");
        $("#inputServerID").focus();
    }
    else if($.trim($('input[name="type"]:checked').val()).length == 0){
        alert("请选择查询条件");
    }
    else{
        gmPost("/server/search_notime/", $(form).serialize(), function(html){
        $("#server-search-notime-table").html(html);
    });
    }
}

function rechargeGetInfo(form){
    if($.trim($("#inputServerID").val()).length == 0){
        alert("请输入服务器ID");
        $("#inputServerID").focus();
    }
    else if($.trim($("#inputUserID").val()).length == 0){
        alert("请输入用户ID");
        $("#inputUserID").focus();
    }
    else{
        gmPost("/recharge/search_recharge/", $(form).serialize(), function(html){
        $("#recharge-search-table").html(html);
        });
    }
}

function sendMessage(form){
    if($.trim($("#inputServerID").val()).length == 0){
        alert("请输入服务器ID");
        $("#inputServerID").focus();
    }
    else if($.trim($("#inputUserID").val()).length == 0){
        alert("请输入用户ID");
        $("#inputUserID").focus();
    }
    else if($.trim($("#inputMessage").val()).length == 0){
        alert("消息不能为空");
        $("#inputMessage").focus();
    }
    else{
        gmPost("/sendmessage/send/", $(form).serialize(), function(html){
        $("#send-message-result").html(html);
        });
    }
}

function elementGetInfo(form){
    if($.trim($("#inputServerID").val()).length == 0){
        alert("请输入服务器ID");
        $("#inputServerID").focus();
    }
    else if($.trim($("#inputUserID").val()).length == 0){
        alert("请输入用户ID");
        $("#inputUserID").focus();
    }
    else{
        gmPost("/element/search_element/", $(form).serialize(), function(html){
        $("#element-search-table").html(html);
        });
    }
}

function deleteelement(form){
        gmPost("/element/delete_element/", $(form).serialize(), function(html){
        $("#delete-element-search-table").html(html);
        });
}

function send_welfare(form){
    if($.trim($("#inputServerID").val()).length == 0){
        alert("请输入服务器ID");
        $("#inputServerID").focus();
    }
    else if($.trim($("#inputUserID").val()).length == 0){
        alert("请输入用户ID");
        $("#inputUserID").focus();
    }
    else{
        gmPost("/welfare/send_welfare/", $("#form1").serialize(), function(html){
        $("#welfare-send-table").html(html);
        });
    }
}

function orderGetInfo(form){
    if($.trim($("#inputServerID").val()).length == 0){
        alert("请输入服务器ID");
        $("#inputServerID").focus();
    }
    else if($.trim($("#inputOrderID").val()).length == 0){
        alert("请输入订单ID");
        $("#inputOrderID").focus();
    }
    else{
        gmPost("/order/search_order/", $(form).serialize(), function(html){
        $("#order-search-table").html(html);
        });
    }
}

function orderFake(form){
    if($.trim($("#inputServerID2").val()).length == 0){
        alert("请输入服务器ID");
        $("#inputServerID").focus();
    }
    else if($.trim($("#inputUserID").val()).length == 0){
        alert("请输入用户ID");
        $("#inputUserID").focus();
    }
    else if($.trim($("#inputRechargeMoney").val()).length == 0){
        alert("请输入充值金额");
        $("#inputRechargeMoney").focus();
    }
    else{
        gmPost("/order/fake_order/", $(form).serialize(), function(html){
        $("#order-fake-result").html(html);
        });
    }
}

function addOrder(serverid,orderid){
    gmPost("/order/add_order/", {server_id:serverid,order_id:orderid}, function(html){
       $("#order-add-result").html(html);
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

function responseEmail(form){
    gmPost("/feedback/response/", $(form).serialize(), function(data){
        $(".game-container").html(data);
    });
}

function sendEmail(form){
    gmPost("/feedback/send_email/", $(form).serialize(), function(data){
    $(".game-container").html(data);
    });
}

function addActivity(form){
    gmPost("/activity/add_activity/", $(form).serialize(), function(data){
    $("#add-activity-result").html(data);
    });
}

function getActivity(form){
    gmPost("/activity/get_activity/", $(form).serialize(), function(data){
    $("#get-activity-result").html(data);
    });
}

function firstPage(){
    gmPost("/check_feedback/1/",{},function(recdata){
    $(".game-container").html(recdata);
    });
}

function previousPage(curpage){
    if(curpage == 1){
        alert("当前已在第一页");
    }
    else{
        gmPost("/check_feedback/"+String(curpage-1)+"/",{},function(recdata){
        $(".game-container").html(recdata);
        });
    }
}

function goPage(page){
    gmPost("/check_feedback/"+String(page)+"/",{},function(recdata){
    $(".game-container").html(recdata);
    });
}

function nextPage(curpage,pagenumber){
    if(curpage == pagenumber){
        alert("当前已在最后一页");
    }
    else{
        gmPost("/check_feedback/"+String(curpage+1)+"/",{},function(recdata){
        $(".game-container").html(recdata);
        });
    }
}

function lastPage(pagenumber){
    gmPost("/check_feedback/"+String(pagenumber)+"/",{},function(recdata){
    $(".game-container").html(recdata);
    });
}
