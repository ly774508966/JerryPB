#!/usr/bin/python
# encoding=utf-8

import xlrd, os, sys
from datetime import datetime
from logger import Logger
from config import Config

logger = Logger(Logger.LOG_LEVEL_INFO, 'myTable')
config = Config()

class MyType(object):
    NORMAL_TYPE_ARR = ['sint32', 'uint32', 'string', 'float']
    

    TYPE_NORAML = 0
    TYPE_USER   = 1
    TYPE_UNKNOW = 2
    
    def __init__(self):
        self.space = ''
        self.prefix = ''
        self.type = MyType.TYPE_UNKNOW
        self.name = 'UNKNOW'
        self.default_val = ''

    @classmethod
    def judge_type(cls, data):
        ret = MyType()
        if data.find('List.') != -1:
            ret.prefix = 'repeated'
            data = data.split('.',1)[1]
        else:
            ret.prefix = 'optional'

        if MyType.NORMAL_TYPE_ARR.count(data) > 0:
            ret.name = data
            ret.type = MyType.TYPE_NORAML
            return ret

        table = xlrd.open_workbook(config.user_type_table_path)
        sheet = table.sheets()[0]
        for i in range(sheet.nrows):
            if i == 0:
                continue
            tname = MyTableTool.to_unicode(sheet.cell(i,0).value)
            if tname == data:
                ret.type = MyType.TYPE_USER
                ret.name = data
                ret.space = MyTableTool.to_unicode(sheet.cell(i,1).value)
                ret.default_val = MyTableTool.to_unicode(sheet.cell(i,2).value)
                return ret
        return ret
            
class MyTableTool(object):
    USE_TYPE_NONE   = 0
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
            pass
            #logger.info('no use type : ' + str(data))
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
        self.name = MyTableTool.to_unicode(column_data[1])
        self.des = MyTableTool.to_unicode(column_data[3])
        
        self.type_name = MyTableTool.to_unicode(column_data[0])
        self.type = MyType.judge_type(self.type_name)

    def is_type(self, use_type):
        ret = False
        if use_type == self.use_type or self.use_type == MyTableTool.USE_TYPE_ALL:
            ret = True
        return ret

    def to_proto(self, use_type, file_handler):
        if self.is_type(use_type) == False:
            return
        if self.type.type == MyType.TYPE_USER and self.type.default_val != '':
            file_handler.write('\t{} {} {} = {} [default = {}]; //{}\n'.format(self.type.prefix, self.type.name, self.name, self.idx, self.type.default_val, self.des))
        else:
            file_handler.write('\t{} {} {} = {}; //{}\n'.format(self.type.prefix, self.type.name, self.name, self.idx, self.des))
        
class MyTableSheet(object):
    def __init__(self, excel_sheet, sheet_idx):

        self.use_type = MyTableTool.get_use_type(excel_sheet.name)
        if self.use_type == MyTableTool.USE_TYPE_NONE:
            return
        
        self.idx = sheet_idx
        self.name = excel_sheet.name.split('_', 1)[1]
        self.columns = []

        for i in range(excel_sheet.ncols):
            column = MyTableColumn(excel_sheet.col_values(i), i)
            if column.use_type != MyTableTool.USE_TYPE_NONE:
                self.columns.append(column)

    def is_type(self, use_type):
        ret = False
        if use_type != self.use_type and self.use_type != MyTableTool.USE_TYPE_ALL:
            return ret
        for column in self.columns:
            if column.is_type(use_type) == True:
                ret = True
                break
        return ret

    def get_space(self, use_type):
        ret = []
        if use_type != self.use_type and self.use_type != MyTableTool.USE_TYPE_ALL:
            return ret
        if self.is_type(use_type) == False:
            return ret
        for column in self.columns:
            if column.type.type == MyType.TYPE_USER and column.type.space != '' and ret.count(column.type.space) <= 0:
                ret.append(column.type.space)
        return ret

    def to_proto(self, use_type, file_handler):
        if use_type != self.use_type and self.use_type != MyTableTool.USE_TYPE_ALL:
            return
        if self.is_type(use_type) == False:
            return
        file_handler.write('message {}\n'.format(self.name))
        file_handler.write('{\n')
        for column in self.columns:
            column.to_proto(use_type, file_handler)
        file_handler.write('}\n\n')

        file_handler.write('message {}_ARRAY\n'.format(self.name))
        file_handler.write('{\n')
        file_handler.write('\trepeated {} rows = 1;\n'.format(self.name))
        file_handler.write('}\n\n')
        
class MyTable(object):
    def __init__(self, excel_path):
        
        self.name = os.path.splitext(os.path.basename(excel_path))[0]
        self.sheets = []
        
        data = xlrd.open_workbook(excel_path)
        for i in range(len(data.sheets())):
            excel_sheet = data.sheets()[i]
            sheet = MyTableSheet(excel_sheet, i)
            if sheet.use_type != MyTableTool.USE_TYPE_NONE and len(sheet.columns) > 0:
                self.sheets.append(sheet)

    def is_type(self, use_type):
        ret = False
        if use_type != MyTableTool.USE_TYPE_CLIENT and use_type != MyTableTool.USE_TYPE_SERVER:
            return ret
        
        for sheet in self.sheets:
            if sheet.is_type(use_type) == True:
                ret = True
                break
        return ret

    def get_space(self, use_type):
        spaces = []

        if use_type != MyTableTool.USE_TYPE_CLIENT and use_type != MyTableTool.USE_TYPE_SERVER:
            return spaces
        if self.is_type(use_type) == False:
            return spaces

        for sheet in self.sheets:
            rets = sheet.get_space(use_type)
            for ret in rets:
                if spaces.count(ret) <= 0:
                    spaces.append(ret)

        return spaces

    def to_proto(self, use_type = MyTableTool.USE_TYPE_CLIENT):
        if use_type != MyTableTool.USE_TYPE_CLIENT and use_type != MyTableTool.USE_TYPE_SERVER:
            return
        if self.is_type(use_type) == False:
            return

        table_prefix = ''
        table_package = ''
        if use_type == MyTableTool.USE_TYPE_CLIENT:
            table_prefix = config.client_table_prefix
            table_package = config.client_table_package
        else:
            table_prefix = config.server_table_prefix
            table_package = config.server_table_package

        with open('{}{}{}.proto'.format(config.proto_path, table_prefix, self.name), 'w') as f:
            f.write('//auto generate by code at {}\n\n'.format(datetime.now().strftime('%Y-%m-%d %I:%M:%S')))
            
            for sp in self.get_space(use_type):
                f.write('import "{}";\n'.format(sp))
            f.write('\n')
            
            if table_package != '':
                f.write('package {};\n'.format(table_package))
            f.write('\n')

            for sheet in self.sheets:
                sheet.to_proto(use_type, f)
            
