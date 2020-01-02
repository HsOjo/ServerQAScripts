#!/usr/bin/env python3
import os
import re
from typing import List, Dict

from geoip import geolite2, IPInfo


def parse_connections(content: str):
    items = re.findall('(\d+\.\d+\.\d+\.\d+):(\d+)-(\d+\.\d+\.\d+\.\d+):(\d+)', content)
    connections = []  # type: List[Dict[str, str]]
    for dest_host, dest_port, src_host, src_port in items:
        connections.append(dict(
            dest_host=dest_host,
            dest_port=int(dest_port),
            src_host=src_host,
            src_port=int(src_port),
        ))

    return connections


def hogs_connections(count=2):
    proc = os.popen('nethogs -t -c %d' % count)
    result = proc.read()  # type: str
    return parse_connections(result)


def ban_ip(ip: str):
    os.system('ufw deny from %s to any' % ip)


count = 2
while True:
    conns = hogs_connections(count)
    for conn in conns:
        src_host = conn['src_host']
        ip = geolite2.lookup(src_host)  # type: IPInfo
        if ip is not None:
            if ip.country != 'CN':
                ban_ip(src_host)
        else:
            print(src_host)

    if len(conns) <= 0:
        count += 1
    elif count > 2:
        count -= 1
