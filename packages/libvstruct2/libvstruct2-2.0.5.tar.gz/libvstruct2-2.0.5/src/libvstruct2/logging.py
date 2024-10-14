"""
libvstruct2: Message output component.

Author: Vlad Topan (vtopan/gmail)
"""

import sys
import time


CFG = {
    'debug_level': 0,
    'timestamps': 0,
    'max_hex_chars': 10,
    }


def timestamp():
    """
    Return current time as log prefix.
    """
    if not CFG['timestamps']:
        return ''
    return time.strftime('<%H:%M:%S> ')


def log(msg):
    """
    Output log message.
    """
    sys.stderr.write(f'{timestamp()}[*] {msg}\n')


def err(msg):
    """
    Output error message.
    """
    sys.stderr.write(f'{timestamp()}[!] {msg}\n')


def warn(msg):
    """
    Output warning message.
    """
    sys.stderr.write(f'{timestamp()}[!] {msg}\n')


def dbg(msg, level=1):
    """
    Output debug message.
    """
    if CFG['debug_level'] >= level:
        sys.stderr.write(f'{timestamp()}[#] {msg}\n')

