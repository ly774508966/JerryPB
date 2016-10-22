#!/usr/bin/python
# encoding=utf-8

import sys
import xlrd
from logger import Logger
from tableMgr import TableMgr, TableColumn

logger = Logger(Logger.LOG_LEVEL_INFO)

def ParseArg(argv):
    if len(argv) < 1:
        return False, None
    return True, argv

def Usage():
    print 'this is Usage()'

def ToUnicode(data):
    if type(data) == str:
        data = data.decode('utf8')
    return data        

if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    success, args = ParseArg(sys.argv)
    if not success:
        Usage()
        exit(-1)

    logger.info('ready')
    
    data = xlrd.open_workbook('test.xlsx')
    table = data.sheets()[0]

    if table.nrows < 4:
        logger.error('less 4 rows')
    else:
        pass

    #logger.info('row:{} col:{}'.format(table.nrows, table.ncols))

    tableMgr = TableMgr(table.name.split('_')[1], table.name.split('_')[0])
    
    for i in range(table.ncols):
        col_type = ToUnicode(table.cell(0,i).value)
        col_name = ToUnicode(table.cell(1,i).value)
        col_use_type = ToUnicode(table.cell(2,i).value)
        col_des = ToUnicode(table.cell(3,i).value)
        col_idx = i + 1
        tableMgr.add_column(col_type, col_name, col_des, col_use_type, col_idx)
    tableMgr.out_file(TableColumn.COLUMN_TYPE_CLIENT)
    tableMgr.out_file(TableColumn.COLUMN_TYPE_SERVER)

    logger.info('finish')

