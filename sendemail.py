#!/usr/bin/python
# -*- coding: UTF-8 -*-

# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header

# sender = 'from@runoob.com'
# receivers = ['429240967@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

# # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
# message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
# message['From'] = Header("菜鸟教程", 'utf-8')
# message['To'] =  Header("测试", 'utf-8')

# subject = 'Python SMTP 邮件测试'
# message['Subject'] = Header(subject, 'utf-8')


# try:
#     smtpObj = smtplib.SMTP('localhost')
#     smtpObj.sendmail(sender, receivers, message.as_string())
#     print "邮件发送成功"
# except smtplib.SMTPException:
#     print "Error: 无法发送邮件"


import smtplib
from email.mime.text import MIMEText
# 定义发送列表
mailto_list=["2450623946@qq.com"]
# 设置服务器名称、用户名、密码以及邮件后缀
mail_host = "smtp.exmail.qq.com"
mail_user = "quanming.zhang@fanyoy.com"
mail_pass = "Fanyou$11"
mail_postfix="qq.com"
# 发送邮件函数
def send_mail(to_list, sub, context):
    '''''
    to_list: 发送给谁
    sub: 主题
    context: 内容
    send_mail("xxx@126.com","sub","context")
    '''
    me = mail_user + "<"+mail_user+">"
    print me
    msg = MIMEText(context)
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        send_smtp = smtplib.SMTP()
        send_smtp.connect(mail_host)
        send_smtp.login(mail_user, mail_pass)
        send_smtp.sendmail(me, to_list, msg.as_string())
        send_smtp.close()
        return True
    except Exception as e:
        print(str(e))
        return False
if __name__ == '__main__':
    print "aaa"
    if (True == send_mail(mailto_list,"subject","context")):
        print ("测试成功")
    else:
        print ("测试失败")
