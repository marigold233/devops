#!/usr/bin/env bash
# 日志记录器

declare -r RED=$(tput setaf 1)
declare -r GREEN=$(tput setaf 2)
declare -r YELLOW=$(tput setaf 3)
declare -r BLUE=$(tput setaf 4)
declare -r PINK=$(tput setaf 5)
declare -r RES=$(tput sgr0)

function logger_init(){
	while [ "${#@}" -gt 0 ]; do
		case $1 in
			-o|--output)
				output_log=${2:-false}
				shift 2
				;;
			-d|--dir)
				log_dir=${2:-""}
				shift 2
				;;
			-p|--prefix)
				log_prefix_name=${2:-""}
				shift 2
				;;
			*)
				echo "Unknown option $1"
				return 1
		esac
	done

	[ $output_log ] || return 0
	[ ! -d $log_dir ] && mkdir -p $log_dir

	export output_log
	export log_file=${log_dir}/${log_prefix_name}_$(date "+%-Y-%m-%d").log
}


function logger() {
	level=$1; msg=$2; write_log=${3-true}

	ipaddress=$(hostname -I | awk '{print $1}')

	info_log="${GREEN}$(date '+%F %T') ${ipaddress} [$level]: $msg${RES}"
	err_log="${RED}$(date '+%F %T') ${ipaddress} [$level]: $msg${RES}"
	debug_log="${YELLOW}$(date '+%F %T') ${ipaddress} [$level]: $msg${RES}"
	warn_log="${PINK}$(date '+%F %T') ${ipaddress} [$level]: $msg${RES}"

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
# 不输出到日志文件里
# logger_init
# logger debug "hello world-1"
# logger warn "hello world-2"

# 输出到日志文件里
# logger_init --output true --dir /tmp --prefix test
# logger err "hello world"
# 只输出到控制台，不输出到日志文件里
# logger info "hello worlaaaad" false

logger_init --output true --dir /tmp --prefix test
info_messages=("Connected to database" "Task completed successfully" "Operation finished" "Initialized application")
while true; do
	random_message=${info_messages[$RANDOM % ${#info_messages[@]}]}
	logger info "$random_message"
	sleep 3
done