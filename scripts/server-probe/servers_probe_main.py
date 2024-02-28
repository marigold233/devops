#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import random
from multiprocessing import Process, freeze_support

import toml
from cachetools import TTLCache, cached
from gevent import socket
from gevent.pool import Pool
from sanic import Sanic
from sanic.log import logger
from sanic.request import Request
from sanic.response import HTTPResponse, json

app = Sanic("servers-probe")
config = toml.load(r"config.toml")
servers = config.get("servers")
cache = TTLCache(maxsize=3, ttl=300)


class ProbePort:
    def __init__(self):
        self.ok = []
        self.fail = []

    def one(self, ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        try:
            sock.connect(
                (
                    ip,
                    port,
                )
            )
            logger.info(f"{ip}:{port} open")
            self.ok.append(ip)
        except socket.error:
            logger.error(f"{ip}:{port} closed")
            self.fail.append(ip)
        finally:
            sock.close()

    def batch(self, ip_list):
        pool = Pool(100)
        tasks = [pool.spawn(self.one, ip, 22) for ip in ip_list]
        pool.join()


def format_servers(_type="success") -> list[dict]:
    all_host = {}
    result = []
    for host in servers.get("v1").split("\n"):
        all_host[host] = 1
    for host in servers.get("v2").split("\n"):
        all_host[host] = 2
    probe = ProbePort()
    probe.batch(list(all_host.keys()))
    # random_or_sort = lambda : _random and random.shuffle(result) or result.sort(key=lambda d: d["host"])
    if _type == "success":
        for h in probe.ok:
            version = all_host[h]
            result.append({"host": h, "port": 6000, "version": version, "weight": 1})
            result.sort(key=lambda d: d["host"])
        return result
    for h in probe.fail:
        version = all_host[h]
        result.append({"host": h, "port": 6000, "version": version, "weight": 1})
    result.sort(key=lambda d: d["host"])
    return result


@cached(cache)
def get_success_servers():
    return format_servers(_type="success")


# @cached(cache)
def get_fail_servers():
    return format_servers(_type="fail")


@app.route("/success", methods=["GET"])
def allservers(request: Request) -> HTTPResponse:
    ret = get_success_servers()
    random.shuffle(ret)
    return json(ret)


@app.route("/fail", methods=["GET"])
def allservers(request: Request) -> HTTPResponse:
    return json(get_fail_servers())


def main():
    app.run(host="0.0.0.0", port=13000, access_log=True)


if __name__ == "__main__":
    freeze_support()
    Process(target=main).start()
