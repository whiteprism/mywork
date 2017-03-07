# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.conf import settings
import os, shutil, commands, cPickle

xls_file_name = "kiwi_ios.xlsx"
make_script_name = "make.sh"
load_script_name = "load.sh"
private_setting = "xsf"
server_ctl_script_name = "server.sh"
module_list_file_name = "load.txt"
xls_file_path = os.path.abspath(os.path.join(settings.ROOT_PATH, "../", "data"))
xls_file = os.path.join(xls_file_path, xls_file_name)
make_script = os.path.join(xls_file_path, make_script_name)
load_script = os.path.join(xls_file_path, load_script_name)
module_list_file = os.path.join(xls_file_path, module_list_file_name)
server_ctl_script = os.path.join(os.path.dirname(xls_file_path), "scripts", private_setting, server_ctl_script_name)


def index(request):
    module_name = []
    # /data/git_repo/kiwibackend/data/load.txt
    with open(module_list_file) as f:
        # 读出每行内容
        for i in f.readlines():
            # 去除每行的行首和行尾的换行符
            j = i.strip('\n')
            if j:
                module_name.append(j)
            # 将所有的名字返回在一个ｌｉｓｔ类型的变量中，传递给模板中的index.html文件。
    return render(request, "index.html", {"module_name": module_name})

def upload(request):
    """
    upload kiwi_ios.xlsx to data dir
    """
    xls = request.FILES["xls"]
    if os.path.isfile(xls_file):
        shutil.copyfile(xls_file, os.path.join(xls_file_path, "backup_" + xls_file_name))
        fh = open(xls_file, "w")
        fh.write(xls.read())
        fh.close()

    #return HttpResponseRedirect(reverse("server_xls_index"))
    return  render(request, 'result.html', {"result": "上传成功"})

def reload_server(request):
    """
    bash ../scripts/xsf/server.sh reload
    """
    if os.path.isfile(server_ctl_script):
        output = commands.getoutput("/bin/bash " + server_ctl_script + " reload")
    return render(request, 'result.html', {"result": output})

def make_json(request):
    # 拿到选中的所有名字
    check_box_list = request.REQUEST.getlist('module_name')
    module_name = ""
    for module in check_box_list:
        # loginbonus:连续登陆　这种形式的
        if ":" in module:
            # 用：分割以后取得第一个字符就是loginbonus
            _m = module.split(":")[0]
        else:
            _m = module
        module_name += "%s " % _m
    cPickle.dump(module_name, open("/tmp/kiwi_modules.pkl", "wb"))
    if os.path.isfile(make_script):
        # 执行shell脚本.将返回的结果传递给下一个页面的result参数。
        output = commands.getoutput("/bin/bash " + make_script + " kiwi " + "'" + module_name + "'")
        # 显示成功的信息。
    return render(request, 'result.html', {"result": output})

def load_json(request):
    """
    bash ./load.sh kiwi settings.SETTINGS 'module_name1 module_name2'
    """
    module_name = cPickle.load(open("/tmp/kiwi_modules.pkl","rb"))
    if os.path.isfile(load_script):
        output = commands.getoutput("/bin/bash " + load_script + " kiwi " + "settings." + private_setting + " '" + module_name + "'")
    return render(request, 'result.html', {"result": output})
