#! /bin/bash

LOCATE=`cd $(dirname $0) && pwd`
HOME="${LOCATE}/../application"
SETTINGS=$1

MODULE_NAME=$2
CLASS_NAME=$3
if [ ! ${MODULE_NAME} ];then
    echo '请输入模块名称!'
    exit 1
fi

cd ${HOME}

if [ ! -f module/${MODULE_NAME}/models.py ]; then
    echo "${HOME}/module/${MODULE_NAME}/models.py不存在，请检查"
    exit 2
fi

gen_yaml(){
    class=$1
    class_low=`echo ${class} | tr 'A-Z' 'a-z'`
#    python manage.py module2yml --m=${MODULE_NAME} --c=${class} --settings=${SETTINGS} && echo "生成${class}成功" || echo "生成${class}失败！"
    python manage.py module2yml --m=${MODULE_NAME} --c=${class} --settings=${SETTINGS} > ../data/yaml/${class_low}.yml && echo "生成${class}成功" || echo "生成${class}失败！"
}

if [ ! ${CLASS_NAME} ] ;then
    CLASSES=`egrep "^class" module/${MODULE_NAME}/models.py | awk -F'(' '{print $1}' | awk '{print $2}'`
    for class in ${CLASSES}
    do
        gen_yaml ${class}
    done
else
    gen_yaml ${CLASS_NAME}
fi


