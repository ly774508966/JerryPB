#!/usr/bin/python
# encoding=utf-8

import sys, os
import xlrd
from logger import Logger
from tableMgr import TableMgr, TableColumn
from config import Config, UserType

config = Config()
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

def DeleteOldProto():
    for parent, dirnames, filenames in os.walk(config.proto_path):
        for filename in filenames:
            if filename.find(config.client_table_prefix) != -1 or filename.find(config.server_table_prefix) != -1:
                os.remove(config.proto_path + filename)

def HandleExcels():
    for parent, dirnames, filenames in os.walk(config.table_path):
        for filename in filenames:
            if filename.find('.xlsx') != -1:
                HandleOneExcel(filename)

def HandleOneExcel(path):
    logger.info('handle excel : ' + path)
    
    data = xlrd.open_workbook(config.table_path + path)
    
    for i in range(len(data.sheets())):
        table = data.sheets()[i]
        HandleOneSheet(table)
    
def HandleOneSheet(table):

    if table.name.find('_') == -1:
        return

    sheet_name = table.name.split('_', 1)[1]
    sheet_type = TableMgr.get_use_type(table.name.split('_', 1)[0])
    if sheet_type == TableColumn.COLUMN_TYPE_NONE:
        return
    
    if table.nrows < 4:
        logger.error('less 4 rows')
    else:
        pass

    #logger.info('row:{} col:{}'.format(table.nrows, table.ncols))

    tableMgr = TableMgr(sheet_name, sheet_type)
    
    for i in range(table.ncols):
        col_type = ToUnicode(table.cell(0,i).value)
        col_name = ToUnicode(table.cell(1,i).value)
        col_use_type = ToUnicode(table.cell(2,i).value)
        col_des = ToUnicode(table.cell(3,i).value)
        col_idx = i + 1
        tableMgr.add_column(col_type, col_name, col_des, col_use_type, col_idx)
    tableMgr.out_file(TableColumn.COLUMN_TYPE_CLIENT)
    tableMgr.out_file(TableColumn.COLUMN_TYPE_SERVER)

if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    success, args = ParseArg(sys.argv)
    if not success:
        Usage()
        exit(-1)

    logger.info('---------------------------------------')
    logger.info('ready')

    DeleteOldProto()
    HandleExcels()

    logger.info('finish')

