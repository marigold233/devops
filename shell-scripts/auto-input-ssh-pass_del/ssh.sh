#!/usr/bin/env bash
# -T 禁止分配伪终端
# -tt 分配一个伪终端
# -q 安静模式，导致大多数警告和诊断消息被禁止显示
export SSH_ASKPASS='/root/my_shell/utils/pass.sh'
export DISPLAY='none:0'
SSH_CONTROL_FILE_PATH='./ssh-cache/'

save_ssh_socket(){
	ip="$1"
	username=${2-root}
	# shellcheck disable=SC2034
	password="$3"
	port=${4-22}
	if ls ${SSH_CONTROL_FILE_PATH}/*"${ip}"* &>/dev/null; then
		return 0
	fi
	setsid ssh -q \
		-o StrictHostKeyChecking=no \
		-o ControlPath=${SSH_CONTROL_FILE_PATH}%h_%p_%r \
		-o ControlMaster=yes \
		-o ControlPersist=yes \
		-p "${port}" "${username}"@"${ip}" <<- EOF
		exit 0
		EOF

}
execute_ssh_cmd(){
	local ip=$1
	local c=$2
	local permission=${3-false}
	# shellcheck disable=SC2034
	local -r ssh_pass=$(cat $SSH_ASKPASS)
	[ "$permission" == "sudo" ] && c=$(echo -e "$c" | sed -e 's/^/sudo /' -e "1i  $(cat $SSH_ASKPASS) | sudo -S -i" -e '1i echo')
	local -r socket_filename=$(ls ${SSH_CONTROL_FILE_PATH}/*"${ip}"*)
	# shellcheck disable=SC2155
	local port=$(awk -F_ '{print $2}' <<< "$socket_filename")
	# shellcheck disable=SC2155
	local username=$(awk -F_ '{print $3}' <<< "$socket_filename")
	setsid ssh -q \
                -o ControlPath=${SSH_CONTROL_FILE_PATH}%h_%p_%r \
                -p "${port}" "${username}"@"${ip}" <<- EOF
		$c
                exit 0
	EOF
}
save_ssh_socket 47.108.187.30 yanghe 
cmd=$(cat <<- EOF
        userdel yanghe
EOF
)
execute_ssh_cmd ip "$cmd" sudo

