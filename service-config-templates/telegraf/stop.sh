: ${1:?}

pkill -u "$1" -f telegraf
pgrep -u "$1" -f telegraf
