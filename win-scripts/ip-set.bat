::参考：https://www.jb51.net/article/26997.htm

netsh interface ip set address name="以太网" source=static addr=10.4.100.213 mask=255.255.255.0 gateway=10.4.101.254
netsh interface ip add dns "以太网" 114.114.114.110 index=1 >nul 
netsh interface ip add dns "以太网" 114.114.113.110 index=2 >nul
