#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket

from gevent.pool import Pool
from gevent import socket
from loguru import logger

# from gevent import monkey; monkey.patch_all()

class ProbePort:
    def one(self, ip, port):
        # sock = socket.socket()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            sock.connect((ip, port,))
            logger.info(f"{ip}:{port} open")
        except socket.error:
            logger.error(f"{ip}:{port} closed")
        finally:
            sock.close()

    def batch(self, ip_list):
       pool = Pool(100)
    #    _ip, _port = ip.split(":")
       def worker(ip):
            _ip, _port = ip.split(":")
            self.one(_ip, int(_port))
       tasks = [pool.spawn(worker, ip) for ip in ip_list]
       pool.join()

if __name__ == "__main__":
    servers = [
        "192.168.12.18:6000",
        "192.168.12.19:6000",
        "192.168.12.20:6000",
        "192.168.12.21:6000",
        "192.168.12.27:6000",
        "192.168.12.28:6000",
        "192.168.12.49:6000",
        "192.168.12.50:6000",
        "192.168.12.57:6000",
        "192.168.12.58:6000",
        "192.168.12.29:6000",
        "192.168.12.30:6000",
        "192.168.12.59:6000",
        "192.168.12.60:6000",
        "192.168.12.65:6000",
        "192.168.12.66:6000",
        "192.168.12.67:6000",
        "192.168.12.68:6000",
        "192.168.12.69:6000",
        "192.168.12.70:6000",
        "192.168.12.71:6000",
        "192.168.12.72:6000",
        "192.168.12.73:6000",
        "192.168.12.74:6000",
        "192.168.12.75:6000",
        "192.168.12.76:6000",
        "192.168.12.77:6000",
        "192.168.12.78:6000",
        "192.168.12.79:6000",
        "192.168.12.80:6000",
        "192.168.12.81:6000",
        "192.168.12.82:6000",
        "192.168.12.83:6000",
        "192.168.12.84:6000",
        "192.168.12.85:6000",
        "192.168.12.86:6000",
        "192.168.12.87:6000",
        "192.168.12.88:6000"
    ]
    probe = ProbePort()
    probe.batch(servers)