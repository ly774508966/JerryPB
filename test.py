#!/usr/bin/python
# encoding=utf-8

import sys
import xlrd

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
    data = xlrd.open_workbook('test.xlsx')
    table = data.sheets()[0]

    nrows = table.nrows
    ncols = table.ncols

    row0 = table.row_values(0)

    if table.cell(0,0).value == 'int':
        print 'a'
    else:
        print 'b'
    print table.cell(0,0).value
    print table.cell(0,0)
    print unicode(u'int')
    print row0
    print nrows
    print ncols

