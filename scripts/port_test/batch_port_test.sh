#!/usr/bin/env bash
source ./logger.sh
logger_init false


main(){
	port=$1
	mapfile -t file_var < ip_list.txt
	for ip in ${file_var[@]}; do
		if ./wait-for-it.sh $ip:$port -t 3 &>/dev/null
		then
			logger info  "$ip:$port is open"
		else
			logger err "$ip:$port is closed"
		fi
	done
}
main $@
