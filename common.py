import subprocess
import sys


def str_compare_head_tail(text, head, tail=None):
    if tail is None:
        tail = head
    return text[:len(head)] == head and text[-len(tail):] == tail


def sub_exec(args, input=None, timeout=None, **kwargs):
    kwargs.setdefault('encoding', sys.getdefaultencoding())
    proc = subprocess.Popen(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, **kwargs)
    return proc.communicate(input, timeout)
