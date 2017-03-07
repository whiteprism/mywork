#! /bin/bash
OPTION=$1
VIRTUAL_ENV=/opt/virtualenvs/kiwi2
LOCATE=`cd $(dirname $0) && pwd`
DIR_NAME=`basename ${LOCATE}`
APP_ROOT=`cd "${LOCATE}/../../application" && pwd`
CONFIG_FILE=${LOCATE}/uwsgi.xml
PID_FILE=`grep "<pidfile>" ${CONFIG_FILE} |awk -F'>' '{print $2}' | awk -F'<' '{print $1}'`


if [ -d ${VIRTUAL_ENV} ]; then
    source ${VIRTUAL_ENV}/bin/activate
else
    echo "虚拟环境不存在！"
    exit 1
fi

usage(){
	echo "usage: $0 {start|stop|restart|reload|create_robot|update_cache_all}"
	exit 1
}

check_option(){
	RESULT=$?
    if [ ${RESULT} -eq 0 ];then
        echo "${DIR_NAME} ${OPTION} succ"
    else
        echo "${DIR_NAME} ${OPTION} fail..."
    fi
}

count_pid(){
	ps aux | grep uwsgi | grep ${LOCATE} | grep -v grep |wc -l
}

start_server(){
	if [ `count_pid` -gt 1 ]; then
		echo "uWSGI is runing!"
	else
		uwsgi -H ${VIRTUAL_ENV} -x ${CONFIG_FILE}
		check_option
	fi
}

stop_server(){
	PIDS=`ps aux | grep uwsgi | grep ${LOCATE} | grep -v grep | awk '{print $2}'`
    if [ ! -z "${PIDS}" ];then
        for i in ${PIDS}
        do
                kill -9 $i
        done
        check_option
    else
        echo "No process, stop fail ..."
        exit 1
    fi
    rm -f ${PID_FILE}
}

restart_server(){
	if [ `count_pid` -gt 1 ]; then
		OPTION="stop"
		stop_server
		OPTION="start"
		start_server
	else
		start_server
	fi
}

reload_server(){
	if [ `count_pid` -gt 1 ]; then
		kill -HUP `cat ${PID_FILE}`
		check_option
	else
		echo "Server is not running!"
		exit 1
	fi
	
}

update_cache_all(){
    cd ${APP_ROOT}
    python manage.py update_cache_all --settings=settings.${DIR_NAME}
    check_option
}

create_robot(){
    cd ${APP_ROOT}
    python manage.py create_ai_player --settings=settings.${DIR_NAME}
    check_option
}

case ${OPTION} in
	"start")
			start_server
			;;
	"stop")
			stop_server
			;;
	"restart")
			restart_server
			;;
	"reload")
			reload_server
			;;
	"update_cache_all")
			update_cache_all
			;;
	"create_robot")
		    create_robot	
			;;
	*)
		usage
		;;
esac
