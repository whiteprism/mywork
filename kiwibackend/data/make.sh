#!/bin/bash

LOCATE=`cd $(dirname $0) && pwd`
cd ${LOCATE}
gameID_Data="kiwi_ios.xlsx"
if [ ! -f $gameID_Data ]
then
    echo "${gameID_Data}不存在"
    exit 1
fi

YML_DIR=yaml

gameID=$1 #游戏平台
gameID_JsonData="json/$gameID"
if [ ! -d $gameID_JsonData ]
then
    mkdir $gameID_JsonData
fi


if [ ! "$2" ]; then
    file_list=`cat load.txt`
    #file_list=`ls ${YML_DIR} | awk -F'.' '{print $1}'`
else
    file_list=$2
fi



for i in ${file_list}
do
    if [ `echo $i | grep ':'` ];then
        yml=`echo $i | awk -F: '{print $1}'`
    else
        yml=$i
    fi
    echo $yml
    python xls2fix.py $gameID_Data -y ${YML_DIR}/${yml}.yml -o $gameID_JsonData/${yml}.json
done
