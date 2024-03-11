FROM fluentd:v1.16-debian-1
USER root
RUN <<EOT
#!/usr/bin/env bash
set -ex
# sudo sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list
echo "deb https://mirrors.aliyun.com/debian/ bullseye main non-free contrib
deb-src https://mirrors.aliyun.com/debian/ bullseye main non-free contrib
deb https://mirrors.aliyun.com/debian-security/ bullseye-security main
deb-src https://mirrors.aliyun.com/debian-security/ bullseye-security main
deb https://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib
deb-src https://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib
deb https://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib
deb-src https://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib" >/etc/apt/sources.list

apt-get update
apt-get install -y build-essential libgeoip-dev autoconf automake libtool libffi-dev 
apt-get autoclean

fluent-gem sources --remove https://rubygems.org/
fluent-gem sources -a https://gems.ruby-china.com/

install_plugin() { fluent-gem install $1 --no-document; }

install_plugin fluent-plugin-elasticsearch
install_plugin fluent-plugin-record-modifier
install_plugin fluent-plugin-grok-parser
install_plugin fluent-plugin-geoip

rm -rf /var/lib/apt/lists/* /var/cache/debconf/* /var/log/* /var/tmp/*
EOT
ADD GeoLite2-City.mmdb /fluentd/GeoLite2-City.mmdb
