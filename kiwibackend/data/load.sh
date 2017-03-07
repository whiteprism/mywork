#!/bin/bash

JSON_DIR=$1
gameSettings=$2
LOCATE=`cd $(dirname $0) && pwd`
TIME=`date +%Y%m%d%H%M%S`


cd ${LOCATE}/../application
if [ ! "$3" ]; then
    file_list=`cat ../data/load.txt`
else
    file_list=${3}
fi

if [ ! "$file_list" ] ; then
    echo "The data does not exist, Please Check!!!"
    exit 1
fi


for i in ${file_list}
do
    if [ `echo $i | grep ':'` ];then
        json=`echo $i | awk -F: '{print $1}'`
    else
        json=$i
    fi
    echo -ne "Load ${json}.json:"
    python manage.py loaddata ../data/json/${JSON_DIR}/${json}.json --settings=$gameSettings
done
python manage.py update_cache_all --settings=$gameSettings

if [[ $gameSettings == "settings.xsf" ]]; then
    cp ./website/mobile/conf/pbconf.bytes /data/pbconf_back/pbconf_${TIME}.bytes
    python manage.py make_json_data --settings=$gameSettings
    find /data/pbconf_back -type f  -ctime +3 -exec rm -f  {} \;
fi
