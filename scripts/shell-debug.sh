#!/usr/bin/env bash
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
BLUE=$(tput setaf 4)
PINK=$(tput setaf 5)
RES=$(tput sgr0)


SHELL_DEBUG(){
	export PS4='${YELLOW}+ DEBUG [line:$LINENO - func:${FUNCNAME[0]-main}]: ${RES}'
	ERRTRAP(){
		set +x
		local lineno=$1
		local exit_code=$2
		echo -e "${RED}+ ERROR [LINE:$lineno]: Error: Command or funcation exited with status $exit_code, run time ${SECONDS}s${RES}"
		set -x
	}
	trap 'ERRTRAP $LINENO $?' ERR
	EXITRAP(){
		set +x
		echo -e "${GREEN}+ INFO total run time: ${SECONDS}s${RES}"
		set -x
	}
	trap 'EXITRAP' EXIT
	#DEBUGTRAP(){
	#	set +x
	#	echo "${YELLOW}+ DEBUG "command": $BASH_COMMAND, exit code: ${?} ${RES}"
	#	set -x
	#}
	#trap 'DEBUGTRAP' DEBUG
        # set -e
        #set -v
        set -o pipefail
	set -x
}
SHELL_DEBUG
source ${1:?}
