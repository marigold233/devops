#!/usr/bin/env bash
# 日志记录器

function logger_init(){
	output_log=${1-false}
	log_dir=${2-""}
	log_prefix_name=${3-""}

	! $output_log && return 0
	log_file=${log_dir}/${log_prefix_name}_$(date "+%-Y-%m-%d").log
	[ ! -d $log_dir ] && mkdir -p $log_dir
	[ ! -f $log_file ] && touch $log_file
}


function logger() {
	level=$1; msg=$2; write_log=${3-true}
	red=$(tput setaf 1)
	green=$(tput setaf 2)
	yellow=$(tput setaf 3)
	blue=$(tput setaf 4)
	pink=$(tput setaf 5)
	res=$(tput sgr0)
	ipaddress=$(hostname -I | awk '{print $1}')
	info_log="${green}$(date '+%F %T') ${ipaddress} [$level]: $msg${res}"
	err_log="${red}$(date '+%F %T') ${ipaddress} [$level]: $msg${res}"
	debug_log="${yellow}$(date '+%F %T') ${ipaddress} [$level]: $msg${res}"
	warn_log="${pink}$(date '+%F %T') ${ipaddress} [$level]: $msg${res}"
       if $write_log && $output_log; then
		case $level in
			info)
				echo $info_log | tee -a $log_file
				;;
                        err)
                                echo $err_log | tee -a $log_file
				;;
                        debug)
                                echo $debug_log | tee -a $log_file
				;;
                        warn)
                                echo $warn_log | tee -a $log_file
				;;
                esac
		return 0
	fi
	case $level in
		info)
			echo $info_log
			;;
		err)
			echo $err_log
			;;
		debug)
			echo $debug_log
			;;
		warn)
			echo $warn_log
			;;
	esac
}

# 用法：
# 只需打印日志，不需要写入日志文件
#logger_init 
#logger err "hello world"
#logger info "hello world"
#logger debug "hello world"
#logger warn "hello world"

# 需要打印日志，需要写入日志文件
#传参：默认false不写入日志，写入日志的目录，日志文件前缀 
logger_init true /tmp test.log
info_messages=("Connected to database" "Task completed successfully" "Operation finished" "Initialized application")
while true; do
	random_message=${info_messages[$RANDOM % ${#info_messages[@]}]}
	logger info "$random_message"
	sleep 3
done
# 如果某条日志日志不想写入到日志文件，只需要后面加入"false"：
#logger warn "hello world" false

