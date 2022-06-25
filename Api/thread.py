# -*- coding: utf-8 -*-
import threading


class Thread:
    '''与线程有关的操作'''
    @staticmethod
    def func_thread(func):
        '''将函数通过线程的方式执行'''
        def set_thread(*args):
            t = threading.Thread(target=func, args=args)
            t.setDaemon(True)
            t.start()
        return set_thread
