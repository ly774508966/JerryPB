#!/usr/bin/python
# encoding=utf-8

import sys
from datetime import datetime

class Logger(object):
    LOG_LEVEL_ERROR = 3
    LOG_LEVEL_WARN  = 2
    LOG_LEVEL_INFO  = 1

    def __init__(self, level):
        self.__level__ = level
        self.__out_file__ = 1

    def __log__(self, level, content):
        print '{}|{}|{}'.format(datetime.now().strftime('%Y-%m-%d %I:%M:%S'), level, content)
        if self.__out_file__ == 1:
            saveout = sys.stdout
            fsock = open('out.log', 'a')
            sys.stdout = fsock
            print '{}|{}|{}'.format(datetime.now().strftime('%Y-%m-%d %I:%M:%S'), level, content)
            sys.stdout = saveout
            fsock.close()

    def set_level(self, level):
        self.__level__ = level

    def info(self, content):
        if self.__level__ <= self.LOG_LEVEL_INFO:
            self.__log__('INFO', content)

    def warn(self, content):
        if self.__level__ <= self.LOG_LEVEL_WARN:
            self.__log__('WARN', content)

    def error(self, content):
        if self.__level__ <= self.LOG_LEVEL_ERROR:
            self.__log__('ERROR', content)
