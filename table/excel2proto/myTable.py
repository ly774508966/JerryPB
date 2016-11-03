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
    def to_unicode(cls, data):
        if type(data) == str:
            data = data.decode('utf8')
        return data   
    
    @classmethod
    def get_use_type(cls, data):
        if data.find('_') != -1:
            data = data.split('_', 1)[0]
        
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
    def __init__(self, column_data, column_idx):

        self.use_type = MyTableTool.USE_TYPE_NONE

        if len(column_data) < 4:
            return

        self.use_type = MyTableTool.get_use_type(MyTableTool.to_unicode(column_data[2]))

        if self.use_type == MyTableTool.USE_TYPE_NONE:
            return
        
        self.idx = column_idx
        self.type = MyTableTool.to_unicode(column_data[0])
        self.name = MyTableTool.to_unicode(column_data[1])
        self.des = MyTableTool.to_unicode(column_data[3])
        
class MyTableSheet(object):
    def __init__(self, excel_sheet, sheet_idx):

        self.use_type = MyTableTool.get_use_type(excel_sheet.name)
        if self.use_type == MyTableTool.USE_TYPE_NONE:
            return
        
        self.idx = sheet_idx
        self.name = excel_sheet.name.split('_', 1)[1]
        self.colums = []

        for i in range(excel_sheet.ncols):
            column = MyTableColumn(excel_sheet.col_values(i), i)
            if column.use_type != MyTableTool.USE_TYPE_NONE:
                self.colums.append(column)
                
        logger.info(sheet_idx)
        logger.info(self.name)

    def to_proto(self):
        pass    

class MyTable(object):
    def __init__(self, excel_path):
        logger.info(excel_path)
        self.name = ''
        self.sheets = []
        
        data = xlrd.open_workbook(excel_path)
        for i in range(len(data.sheets())):
            excel_sheet = data.sheets()[i]
            sheet = MyTableSheet(excel_sheet, i)
            if sheet.use_type != MyTableTool.USE_TYPE_NONE and len(sheet.colums) > 0:
                self.sheets.append(sheet)

    def to_proto(self):
        logger.info('name:{}'.format(self.name))
        #for sheet in self.sheets:
            
            
