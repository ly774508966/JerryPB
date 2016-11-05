#!/usr/bin/python
# encoding=utf-8

import sys, os
import xlrd
from logger import Logger
from myTable import MyTable, MyTableTool
from config import Config

config = Config()
logger = Logger(Logger.LOG_LEVEL_INFO, 'excel2proto')

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
            if filename.find('.xlsx') != -1 and filename.find('scene') != -1:
                table = MyTable(parent + filename)
                table.to_proto(MyTableTool.USE_TYPE_CLIENT)
                #table.to_proto(MyTableTool.USE_TYPE_SERVER)

if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    success, args = ParseArg(sys.argv)
    if not success:
        Usage()
        exit(-1)

    logger.reset()
    logger.info('ready')

    DeleteOldProto()
    HandleExcels()

    logger.info('finish')

