#!/usr/bin/env bash
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
BLUE=$(tput setaf 4)
PINK=$(tput setaf 5)
RES=$(tput sgr0)


function logger_init(){
	output_log=${1-false}
	log_dir=${2-""}
	log_prefix_name=${3-""}
	if  ! $output_log; then
		return 0
	fi
	log_file=${log_dir}/${log_prefix_name}_$(date "+%-Y-%m-%d").log
	[ ! -d $log_dir ] && mkdir -p $log_dir
	[ ! -f $log_file ] && touch $log_file
}


function logger() {
       level=$1; msg=$2; write_log=${3-true}
       info_log="${GREEN}$(date '+%F %T') [$level]: $msg${RES}"
       err_log="${RED}$(date '+%F %T') [$level]: $msg${RES}"
       debug_log="${YELLOW}$(date '+%F %T') [$level]: $msg${RES}"
       warn_log="${PINK}$(date '+%F %T') [$level]: $msg${RES}"
		if $write_log && $output_log; then
			case $level in
                                info)
                                        echo $info_log | tee -a $log_file;;
                                err)
                                        echo $err_log | tee -a $log_file;;
                                debug)
                                        echo $debug_log | tee -a $log_file;;
                                warn)
                                        echo $warn_log | tee -a $log_file;;
					
                        esac
		else
			case $level in
				info)
					echo $info_log;;
				err)
					echo $err_log;;
                                debug)
                                        echo $debug_log;;
                                warn)
                                        echo $warn_log;;
			esac
		fi					
}
