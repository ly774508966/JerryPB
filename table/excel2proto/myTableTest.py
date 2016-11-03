#!/usr/bin/python
# encoding=utf-8

import sys
from myTable import MyTable, MyTableSheet, MyTableColumn, MyTableTool

def ParseArg(argv):
    if len(argv) < 1:
        return False, None
    return True, argv

def Usage():
    print 'this is Usage()'

if __name__ == '__main__':
    success, args = ParseArg(sys.argv)
    if not success:
        Usage()
        exit(-1)
    print 'start'

    table = MyTable('../table/test.xlsx')
