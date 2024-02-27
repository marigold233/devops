CONFIG=/data/monitor-services/telegraf-1.27.3/etc/telegraf/telegraf.conf
CONFIG_DIR=
PID_FILE=

# default start command:
#telegraf -pidfile /var/run/telegraf/telegraf.pid -config /etc/telegraf/telegraf.conf -config-directory /etc/telegraf/telegraf.d

nohup ./telegraf -config "$CONFIG" &
