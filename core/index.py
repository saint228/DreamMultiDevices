# -*- coding: utf-8 -*-
__author__ = "无声"

import time
from core import MultiAdb as Madb


_print = print
def print(*args, **kwargs):
    _print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), *args, **kwargs)

def main():
    madb=Madb.MultiAdb()
    madb.connectdevices()






