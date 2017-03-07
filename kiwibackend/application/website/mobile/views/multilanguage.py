# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.conf import settings
import os, shutil, commands

multilanguage_root = os.path.abspath(os.path.join(settings.ROOT_PATH, "../", "data", "multiLanguage"))
string_all_file = os.path.join(multilanguage_root, "string_all.txt")
string_update_file= os.path.join(multilanguage_root, "string_update.txt")
xls_file = os.path.join(multilanguage_root, "multiLanguage.xls")
xls_update_file = os.path.join(multilanguage_root, "multiLanguage_update.xls")
script_file = os.path.join(multilanguage_root, "xlsxml.py")
kiwi_git_stable_path = "/data/git_repo/kiwi3d/Assets/Resources/Strings"
kiwi_git_active_path = "/data/git_repo/kiwi3d/Assets/zPkgBundle"

def index(request):
    xls_url = "http://192.168.1.58:81/multiLanguage.xls"
    xls_update_url = "http://192.168.1.58:81/multiLanguage_update.xls"
    string_all_url = "http://192.168.1.58:81/string_all.txt"
    string_update_url = "http://192.168.1.58:81/string_update.txt"
    return render(request, "multilanguage.html", {"xls_url": xls_url, "string_all_url": string_all_url, "xls_update_url": xls_update_url, "string_update_url": string_update_url})

def file_type(file_name):
    out = commands.getoutput("/usr/bin/file" + ' ' + file_name)
    if "text" in out.lower():
        type = "text"
    elif "document" in out.lower():
        type = "xls"
    else:
        type = "other"
    return type

def git_commit_string_all():
    os.chdir(kiwi_git_stable_path)
    stat, out = commands.getstatusoutput("git pull")
    if 0 == stat:
        shutil.copy(string_all_file, "strings.txt")
        git_status = commands.getoutput("git status")
        if "strings.txt" in git_status:
            os.system('git commit -am "multilanguage strings"')
            stat, out = commands.getstatusoutput("git push")
            if 0 == stat:
                msg = "string_all文件已成功提交到前端git"
            else:
                msg = "string_all文件提交失败，请联系网管\nDebug:\n%s" % out
        else:
            msg = "string_all文件没有变化"
    else:
        msg = "git pull出错，请联系网管\nDebug:\n%s" % out
    return msg

def git_commit_string_update():
    os.chdir(kiwi_git_active_path)
    stat, out = commands.getstatusoutput("git pull")
    if 0 == stat:
        shutil.copy(string_update_file, "string_update.txt")
        git_status = commands.getoutput("git status")
        du_status = commands.getoutput("du -ah *")
        fh = open("/tmp/git_du_status.tmp", "w")
        fh.write(git_status + '\n' + du_status )
        fh.close()
        if "string_update.txt" in git_status:
            os.system('git commit -am "multilanguage string_update"')
            stat, out = commands.getstatusoutput("git push")
            if 0 == stat:
                msg = "string_update文件已成功提交到前端git"
            else:
                msg = "string_update文件提交失败，请联系网管\nDebug:\n%s" % out
        else:
            msg = "string_update文件没有变化"
    else:
        msg = "git pull出错，请联系网管\nDebug:\n%s" % out
    return msg

def mix_txt_and_xls(request):
    tmp_file = "/tmp/multilanguage_file"
    try:
        file = request.FILES["upload_file"]
        # print file.field_name, file.name
        file_name = file.name
        fh = open(tmp_file, "w")
        fh.write(file.read())
        fh.close()
        if "text" == file_type(tmp_file):
            if file_name == "string_all.txt":
                shutil.copy(tmp_file, string_all_file)
                os.chdir(multilanguage_root)
                stat, out = commands.getstatusoutput(script_file + " " + string_all_file)
                if 0 == stat:
                    msg = git_commit_string_all()
                    msg = "稳定版Excel文件生成成功," + str(msg)
                else:
                    msg = "稳定版Excel文件生成失败, 请联系网管\nDebug:\n%s" % out
            elif file_name == "string_update.txt":
                shutil.copy(tmp_file, string_update_file)
                os.chdir(multilanguage_root)
                stat, out = commands.getstatusoutput(script_file + " " + string_update_file)
                if 0 == stat:
                    msg = git_commit_string_update()
                    msg = "活跃版Excel文件生成成功," + str(msg)
                else:
                    msg = "活跃版Excel文件生成失败, 请联系网管\nDebug:\n%s" % out
            else:
                msg = "上传的文件名不对!"

        elif "xls" == file_type(tmp_file):
            if file_name == "multiLanguage.xls":
                shutil.copy(tmp_file, xls_file)
                os.chdir(multilanguage_root)
                stat, out = commands.getstatusoutput(script_file + " " + xls_file)
                if 0 == stat:
                    msg = git_commit_string_all()
                    msg = "Excel文件转换成string_all成功," + str(msg)
                else:
                    msg = "Excel文件转换成string_all失败, 请联系网管\nDebug:\n%s" % out
            elif file_name == "multiLanguage_update.xls":
                shutil.copy(tmp_file, xls_update_file)
                os.chdir(multilanguage_root)
                stat, out = commands.getstatusoutput(script_file + " " + xls_update_file)
                if 0 == stat:
                    msg = git_commit_string_update()
                    msg = "Excel文件转换成string_update.txt成功," + str(msg)
                else:
                    msg = "Excel文件转换成string_update.txt失败, 请联系网管\nDebug:\n%s" % out
            else:
                msg = "上传的文件名不对！"
        else:
            msg = "操作失败，可能是上传的文件有问题"
    except:
        msg = "二货，谁让你直接点上传的？！"
    return render(request, "result.html", {"result": msg})

