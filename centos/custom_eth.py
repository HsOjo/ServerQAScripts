#!/usr/bin/env python3
from utils.config_simple import SimpleConfig
import os

CONFIG_GRUB = '/etc/default/grub'
NET_SCRIPTS_DIR = '/etc/sysconfig/network-scripts'


def enable_custom_ether_name():
    with open(CONFIG_GRUB) as io:
        sc = SimpleConfig(io.read())

    if 'net.ifnames' not in sc['GRUB_CMDLINE_LINUX'] and 'biosdevname' not in sc['GRUB_CMDLINE_LINUX']:
        sc['GRUB_CMDLINE_LINUX'] = '''%s net.ifnames=0 biosdevname=0''' % sc['GRUB_CMDLINE_LINUX']

        # Backup raw to comment.
        index = sc.index('GRUB_CMDLINE_LINUX')
        sc.insert(index, {'raw': '# %s' % sc.object(index)['raw']})
        content = sc.text

        with open(CONFIG_GRUB, 'w') as io:
            io.write(content)

        os.system('grub2-mkconfig -o /boot/grub2/grub.cfg')


def rename_ether(old, new):
    path_old = '%s/ifcfg-%s' % (NET_SCRIPTS_DIR, old)
    path_new = '%s/ifcfg-%s' % (NET_SCRIPTS_DIR, new)

    with open(path_old) as io:
        sc = SimpleConfig(io.read())

    sc['NAME'] = new
    sc['DEVICE'] = new

    content = sc.text
    with open(path_new, 'w') as io:
        io.write(content)


old = input('input old ether name:')
new = input('input new ether name:')

enable_custom_ether_name()
rename_ether(old, new)
