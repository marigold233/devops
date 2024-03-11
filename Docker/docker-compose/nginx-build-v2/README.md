
## nginx-build
使用centos6.6系统编译nginx，glibc版本如下，在大于等于该glibc版本的linux理论都可以使用。
```bash
[root@1a5666784713 /]# ldd --version
ldd (GNU libc) 2.12
Copyright (C) 2010 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
Written by Roland McGrath and Ulrich Drepper.
```

## 使用
```bash
docker pull registry.cn-hangzhou.aliyuncs.com/yh-nb/nginx-build:v2
docker run --rm \
  -e NGINX_PREFIX=/data/nginx \
  -e STDOUT=TRUE \
  -e ZLIB_VERSION="1.2.12" \
  -e PCRE_VERSION="8.01" \
  -e OPENSSL_VERSION="1.1.1p" \
  -e NGINX_VERSION="1.22.0" registry.cn-hangzhou.aliyuncs.com/yh-nb/nginx-build:v2 > nginx-bin.tgz
```
如果不指定zlib、pcre、openssl、nginx其中某个版本，默认使用最新的版本进行编译
```bash
docker run --rm \
  -e NGINX_PREFIX=/data/nginx \
  -e STDOUT=TRUE registry.cn-hangzhou.aliyuncs.com/yh-nb/nginx-build:v2 > nginx-bin.tgz
```

- STDOUT=TRUE                输出到标准输出（必须）
- TRACE=TRUE                 debug脚本（非必须）
- ZLIB_VERSION="version"     指定zlib版本（非必须）
- PCRE_VERSION="version"     指定pcre版本（非必须）
- NGINX_VERSION="version"    指定nginx版本（非必须）
- NGINX_PREFIX="version"     指定安装路径（必须）

## 更新
重新用容器编译，然后直接替换旧版本的NGINX即可，注意提前备份

## DEBUG
```diff
docker run --rm \
  -e NGINX_PREFIX=/data/nginx \
+  -e TRACE=TRUE \
  -e STDOUT=TRUE \
  -e ZLIB_VERSION="1.2.12" \
  -e PCRE_VERSION="8.01" \
  -e OPENSSL_VERSION="1.1.1p" \
  -e NGINX_VERSION="1.22.0" registry.cn-hangzhou.aliyuncs.com/yh-nb/nginx-build:v2 > nginx-bin.tgz
```

## Note
### 迁移nginx
编译过nginx查询安装路径，路径为prefix部分：
```bash
root@debian:~/nginx/sbin# ./nginx -h
nginx version: nginx/1.22.1
Usage: nginx [-?hvVtTq] [-s signal] [-p prefix]
             [-e filename] [-c filename] [-g directives]

Options:
  -?,-h         : this help
  -v            : show version and exit
  -V            : show version and configure options then exit
  -t            : test configuration and exit
  -T            : test configuration, dump it and exit
  -q            : suppress non-error messages during configuration testing
  -s signal     : send signal to a master process: stop, quit, reopen, reload
  -p prefix     : set prefix path (default: /software/nginx/)
  -e filename   : set error log file (default: logs/error.log)
  -c filename   : set configuration file (default: conf/nginx.conf)
  -g directives : set global directives out of configuration file
```
迁移nginx到其它目录，比如迁移到~ :
```bash
mv /path/nginx ~/nginx
cd ~/nginx/sbin
./nginx -p ~/nginx # start
./nginx -t -p ~/nginx # check config
./nginx -s stop -p ~/nginx # stop
```
### 用docker编译出现139code容器退出
linux的解决方式：https://blog.csdn.net/weixin_43886198/article/details/111144854  
wsl2的解决方式：
- https://marigold233.github.io/2022/10/20/DockerDesktop%E5%87%BA%E7%8E%B0exit-139%E7%9A%84%E9%94%99%E8%AF%AF/
- https://learn.microsoft.com/zh-cn/windows/wsl/wsl-config#example-wslconfig-file

### 使用普通用户systemd管理nginx
CentOS7是不能用`systemctl --user`的，所以不能普通用户的`systemd`来管理，或许升级`systemd`可以解决？
```bash
mkdir -p ~/.config/systemd/user
cd ~/.config/systemd/user
vim nginx.service
```
Unit 文件：
```ini
[Unit]
Description=The NGINX HTTP and reverse proxy server
After=syslog.target network-online.target remote-fs.target nss-lookup.target
Wants=network-online.target

[Service]
Type=forking
#PIDFile=/usr/local/nginx/nginx.pid
ExecStartPre=/usr/local/nginx/sbin/nginx -t
ExecStart=/usr/local/nginx/sbin/nginx
ExecReload=/usr/local/nginx/sbin/nginx -s reload
#ExecStop=/bin/kill -s QUIT $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```
启动：
```bash
systemctl --user daemon-reload
systemctl --user start nginx.service
systemctl --user status nginx.service
```
参考: 
unit file：https://www.nginx.com/resources/wiki/start/topics/examples/systemd/  
buildx另外一种多平台编译方式：https://zhangguanzhang.github.io/2022/01/26/nginx-static-build/#/%E6%89%8B%E5%8A%A8%E6%AD%A5%E9%AA%A4
