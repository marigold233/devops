telnet：busybox-extras
net-tools: net-tools
tcpdump: tcpdump
wget: wget
dig nslookup: bind-tools
curl: curl
nmap: nmap
wget ifconfig nc traceroute.. : busybox
ssh: openssh-client
ss iptables: iproute2
ethtool: ethtool

使用：
```bash
docker build -t network-tools:latest .
```
关于 `apk add --virtual .persistent-deps gcc gcc-c++` 的解释：
```
 -t, --virtual NAME    Create virtual package NAME with given dependencies
```
当我软件构建好后不需要这些软件包的时候我完全可以删除：
```bash
apk del .persistent-deps
```

参考：
- https://blog.csdn.net/qq_34018840/article/details/94430584
- https://www.oomspot.com/post/alpineanzhuangwangluogongju
