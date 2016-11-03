#!/usr/bin/python
# encoding=utf-8

import xlrd
from logger import Logger

logger = Logger(Logger.LOG_LEVEL_INFO, 'myTable')

class MyTableTool(object):
    USE_TYPE_NONE = 0
    USE_TYPE_CLIENT = 1
    USE_TYPE_SERVER = 2
    USE_TYPE_ALL    = 3
    
    def __init__(self):
        pass
    
    @classmethod
    def get_use_type(cls, data):
        ret = MyTableTool.USE_TYPE_NONE
        if data == 'all':
            ret = MyTableTool.USE_TYPE_ALL
        elif data == 'client':
            ret = MyTableTool.USE_TYPE_CLIENT
        elif data == 'server':
            ret = MyTableTool.USE_TYPE_SERVER    
        elif data == 'none':
            ret = MyTableTool.USE_TYPE_NONE
        else:
            logger.info('no use type : ' + str(data))
        return ret

class MyTableColumn(object):
    def __init__(self):
        self.idx = 0
        self.name = ''
        self.des = ''
        self.type = ''
        self.use_type = MyTableTool.TABLE_TYPE_NONE

class MyTableSheet(object):
    def __init__(self, excel_sheet, sheet_idx):
        self.idx = sheet_idx
        self.name = excel_sheet.name
        self.use_type = MyTableTool.TABLE_TYPE_NONE
        self.colums = []

        logger.info(sheet_idx)

class MyTable(object):
    def __init__(self, excel_path):
        logger.info(excel_path)
        self.name = ''
        self.sheets = []
        data = xlrd.open_workbook(excel_path)
        for i in range(len(data.sheets())):
            excel_sheet = data.sheets()[i]
            sheet = MyTableSheet(excel_sheet, i)
            
