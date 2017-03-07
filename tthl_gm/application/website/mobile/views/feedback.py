# -*- coding: utf-8 -*
from django.contrib.admin.views.decorators import  staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext
import urllib, urllib2
from module.feedback.api import *
import math
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings

def get_feedback_info(request):
    playerinfo = request.POST
    insert_feedback(playerinfo)

@staff_member_required
def check_feedback(request,page):
    show_count = 3.0
    show_count_int = int(show_count)
    page = int(page)
    if page <= 0:
        page = 1
    start = show_count_int*(page-1)
    end = show_count_int*page
    infos = UserFeedback.objects.order_by("-send_time")[start:end]
    infonumber = UserFeedback.objects.count()
    pagenumber = math.ceil(infonumber/show_count)
    pagenumber = int(pagenumber)
    st = 1
    en = pagenumber
    if page <= 10:
        if pagenumber > 20:
            en = 20
    elif page > 10:
        st = page - 10
        en = page + 9
    if page <= pagenumber and page > pagenumber - 10:
        if pagenumber >= 20:
            st = pagenumber - 19
    if en > pagenumber:
        en = pagenumber
    pagelist = range(st,en+1)
    resdata = {
    "curpage":page,
    "infos":infos,
    "pagenumber":pagenumber,
    "pagelist":pagelist
    }
    print resdata,"***"
    ctxt = RequestContext(request,resdata)
    return render_to_response("model/feedback.html",ctxt)

def response(request):
    recdata = request.POST
    email = recdata["email"]
    message = recdata["message"]
    resdata = {
    "email":email,
    "message":message,
    }
    ctxt = RequestContext(request,resdata)

    return render_to_response("feedback/response.html",ctxt)

def send_email(request):
    mail_host = "smtp.exmail.qq.com"
    mail_user = "support@bakusan-genryo.com"
    mail_pass = "Fanyou123"
    recdata = request.POST
    send_to = recdata["email"]
    #context = recdata["response"].encode("utf-8")
    context = recdata["response"]
    to_list = [send_to]
    me = mail_user + "<"+mail_user+">"
    msg = MIMEMultipart()
    #msg = MIMEText(context,'plain','utf-8')
    msg['Subject'] = u"天天幻灵游戏反馈回复"
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    msg.attach(MIMEText(context,'plain','utf-8'))
    result = True
    try:
        send_smtp = smtplib.SMTP()
        send_smtp.connect(mail_host)
        send_smtp.login(mail_user, mail_pass)
        send_smtp.sendmail(me, to_list, msg.as_string())
        send_smtp.close()
    #except (Exception, e):
    except Exception as e:
        print(str(e))
        result = False
    if result:
        update_flag(recdata["email"],recdata["message"])
        resdata = {
        "ret":0,
        "msg":u"邮件发送成功",
        }
    else:
        resdata = {
        "ret":1,
        "msg":u"邮件发送失败",
        }
    ctxt = RequestContext(request,resdata)
    return render_to_response("result.html",ctxt)
