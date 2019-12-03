import os
import re


def list_ethers():
    ethers = []
    str_ip_addr = os.popen('ip addr').read()
    matchs = re.findall('\d+: (.*?):.*?\n.*?link/ether (.*?) ', str_ip_addr)
    for name, mac in matchs:
        ethers.append(dict(name=name, mac=mac))

    return ethers
