#!/bin/bash

JSON_DIR=$1
gameSettings=$2
LOCATE=`cd $(dirname $0) && pwd`

cd ${LOCATE}/../application
file_list=${3}

if [ ! "$file_list" ] ; then
    echo "The data does not exist, Please Check!!!"
    exit 1
fi


for i in ${file_list}
do
    echo -ne "Load package_${i}.json:"
    python manage.py loaddata ../data/json/${JSON_DIR}/packages/package_${i}.json --settings=$gameSettings
done
