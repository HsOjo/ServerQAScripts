#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import time

DATA_FILE = '/tmp/scrvctl.dat'

DEBUG = False


def load_data():
    data = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as io:
            data = json.load(io)  # type: dict
    return data


def dump_data(data: dict):
    with open(DATA_FILE, 'w') as io:
        json.dump(data, io)


def sp_run(*args, v_exit=False, v_out=False):
    if DEBUG:
        print('[Debug] %s' % ' '.join(args))
    if v_out:
        cp = subprocess.run(args, stdout=sys.stdout, stderr=sys.stderr)
    else:
        cp = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if v_exit:
        print('Process finished with exit code %d' % cp.returncode)
    return cp.returncode == 0


class Service:
    def __init__(self, name, args):
        self.name = name
        self.args = args
        sp_run('screen', '-wipe')

    @property
    def screen(self):
        return ['screen', '-S', 'scrv_%s' % self.name]

    @property
    def cmd(self):
        if isinstance(self.args, str):
            cmd = self.args
        else:
            cmd = ' '.join(self.args)

        return cmd

    @staticmethod
    def execute(cmd):
        return ['-X', 'stuff', cmd + r'\n']

    def start(self):
        print(' * Starting %s' % self.name, end='\t')

        if self.is_running:
            print('[OK]')
            return True

        r = sp_run(*self.screen, '-dm', v_exit=False) and sp_run(*self.screen, *self.execute(self.cmd))

        print('[%s]' % 'OK' if r else 'Failed')

        return r

    def stop(self, force=False):
        print(' * Stopping %s' % self.name, end='\t')

        if not self.is_running:
            print('[OK]')
            return True

        r = sp_run(*self.screen, *self.execute('^z' if force else '^c' + r'\nexit'))
        while self.is_running and not force:
            time.sleep(0.1)
            r = self.stop(force=True)

        print('[%s]' % 'OK' if r else 'Failed')

        return not self.is_running

    def restart(self):
        return self.stop() and self.start()

    def status(self, **kwargs):
        kwargs['v_out'] = kwargs.get('v_out', True)
        return sp_run(*self.screen, '-list', **kwargs)

    def into(self):
        return sp_run(*self.screen, '-x')

    @property
    def is_running(self):
        return self.status(v_out=False, v_exit=False)


try:
    if '--debug' in sys.argv:
        DEBUG = True
        sys.argv.remove('--debug')

    data = load_data()
    
    command = sys.argv[1]
    name = sys.argv[2]
    args = sys.argv[3:] or os.getenv('SCRV_ARGS') or data.get(name)

    getattr(Service(name, args), command)()

    if command == 'start':
        data[name] = args
        dump_data(data)
except IndexError as e:
    print('''%a
    Usage:
        %s [command] [service] [args ...]
    Command:
        start
        stop
        restart
        status
        into
    Service:
        (Custom Service Name)
    Args:
        (Custom Service Launch Args)
        
    This script need "screen" to run normally.''' % (e, os.path.basename(__file__)))
