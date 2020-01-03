#!/usr/bin/env python3
import re
import time
from typing import List, Dict

from geoip import geolite2, IPInfo

import common


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
    [out, err] = common.sub_exec('nethogs -t -c %d' % count)
    return parse_connections(out)


def ban_ip(ip: str):
    [out, err] = common.sub_exec('ufw insert 1 deny from %s to any' % ip)
    return 'inserted' in out


count = 2
while True:
    conns = hogs_connections(count)
    for conn in conns:
        src_host = conn['src_host']
        ip = geolite2.lookup(src_host)  # type: IPInfo

        country = None
        if ip is not None:
            country = ip.country

        if country != 'CN':
            if ban_ip(src_host):
                print('%s Ban IP: [%s] %s' % (time.ctime(), country, src_host))

    if len(conns) <= 0:
        count += 1
    elif count > 2:
        count -= 1
