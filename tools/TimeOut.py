# -*- coding: utf-8 -*-
__author__ = "无声"

import threading
import sys


class KThread(threading.Thread):

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


class Timeout(Exception):

    def timeout(seconds):

        def timeout_decorator(func):

            def _new_func(oldfunc, result, oldfunc_args, oldfunc_kwargs):
                result.append(oldfunc(*oldfunc_args, **oldfunc_kwargs))

            def _(*args, **kwargs):
                result = []
                new_kwargs = {
                    'oldfunc': func,
                    'result': result,
                    'oldfunc_args': args,
                    'oldfunc_kwargs': kwargs
                }
                thd = KThread(target=_new_func, kwargs=new_kwargs)
                thd.start()
                thd.join(seconds)
                alive = thd.isAlive()
                thd.kill()
                if alive:
                    raise Timeout(u'function run too long, timeout %d seconds.' % seconds)
                elif thd.exception is not None:
                    raise thd.exception
                return result[0]

            _.__name__ = func.__name__
            _.__doc__ = func.__doc__
            return _

        return timeout_decorator