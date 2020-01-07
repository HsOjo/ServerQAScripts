#!/usr/bin/env python3
import re
import time
from typing import List, Dict, Any

from geoip import geolite2, IPInfo

import common


def parse_connections(content: str):
    items = re.findall('(\d+\.\d+\.\d+\.\d+):(\d+)-(\d+\.\d+\.\d+\.\d+):(\d+)', content)
    connections = []  # type: List[Dict[str, Any]]
    for dest_ip, dest_port, src_ip, src_port in items:
        connections.append(dict(
            dest_ip=dest_ip,
            dest_port=int(dest_port),
            src_ip=src_ip,
            src_port=int(src_port),
        ))

    return connections


def hogs_connections(count=2):
    [out, err] = common.sub_exec('nethogs -t -c %d' % count)
    return parse_connections(out)


def ban_ip(ip: str):
    [out, err] = common.sub_exec('ufw insert 1 deny from %s to any' % ip)
    return 'inserted' in out


count = 2
while True:
    conns = hogs_connections(count)
    for conn in conns:
        src_ip = conn['src_ip']
        ip = geolite2.lookup(src_ip)  # type: IPInfo

        country = None
        if ip is not None:
            country = ip.country

        if conn['src_port'] > 1024:
            if ban_ip(src_ip):
                print('%s Ban IP: [%s] %s' % (time.ctime(), country, src_ip))

    if len(conns) <= 0:
        count += 1
    elif count > 2:
        count -= 1
