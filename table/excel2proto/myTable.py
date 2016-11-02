#!/usr/bin/python
# encoding=utf-8

from logger import Logger
from config import Config, UserType

logger = Logger(Logger.LOG_LEVEL_INFO)
config = Config()

class MyTableTool(object):
    TABLE_TYPE_NONE = 0
    TABLE_TYPE_CLIENT = 1
    TABLE_TYPE_SERVER = 2
    TABLE_TYPE_ALL    = 3
    
    def __init__(self):
        pass

class MyTableColumn(object):
    def __init__(self):
        self.idx = 0
        self.name = ''
        self.des = ''
        self.type = ''
        self.use_type = MyTableTool.TABLE_TYPE_NONE

class MyTableSheet(object):
    def __init__(self):
        self.idx = 0
        self.name = ''
        self.use_type = MyTableTool.TABLE_TYPE_NONE
        self.colums = []

class MyTable(object):
    def __init__(self):
        self.name = ''
        self.sheets = []

    @classmethod
    def get_use_type(cls, data):
        ret = TableColumn.COLUMN_TYPE_NONE
        if data == 'all':
            ret = TableColumn.COLUMN_TYPE_ALL
        elif data == 'client':
            ret = TableColumn.COLUMN_TYPE_CLIENT
        elif data == 'server':
            ret = TableColumn.COLUMN_TYPE_SERVER    
        elif data == 'none':
            ret = TableColumn.COLUMN_TYPE_NONE
        else:
            logger.info('no use type : ' + str(data))
        return ret

    def __get_import__(self, out_type):
        ret = []
        for col in self.columns:
            if col.use_type != out_type and col.use_type != TableColumn.COLUMN_TYPE_ALL:
                continue
            judge_code = config.judge_user_type(col.type2)
            if judge_code == 1:
                user_type = config.get_user_type(col.type2)
                if ret.count(user_type.define_file) <= 0:
                    ret.append(user_type.define_file)
            elif judge_code == -1:
                logger.error('type "{}" not define, in table "{}" column {} "{}"'.format(col.type2, self.name,col.idx , col.name))
        return ret

    def __judge_type__(self, column, col_type):
        #注意，类型本身可能含有'.'
        if col_type.find('List.') != -1:
            column.type1 = 'repeated'
            column.type2 = col_type.split('.',1)[1]
        else:
            column.type1 = 'optional'
            column.type2 = col_type
        return column

    def add_column(self, col_type, col_name, col_des, col_use_type, col_idx):
        use_type = TableMgr.get_use_type(col_use_type)
        if use_type == TableColumn.COLUMN_TYPE_NONE:
            return
        
        column = TableColumn();
        column.name = col_name
        column.idx = col_idx
        column.des = col_des
        column.use_type = use_type
        column = self.__judge_type__(column, col_type)
        
        self.columns.append(column)
        
    def out_file(self, out_type):

        if self.use_type != out_type and self.use_type != TableColumn.COLUMN_TYPE_ALL:
            return

        table_prefix = ''
        table_package = ''
        if out_type == TableColumn.COLUMN_TYPE_CLIENT:
            table_prefix = config.client_table_prefix
            table_package = config.client_table_package
        elif out_type == TableColumn.COLUMN_TYPE_SERVER:
            table_prefix = config.server_table_prefix
            table_package = config.server_table_package
        else:
            return
        
        with open('{}{}{}.proto'.format(config.proto_path, table_prefix, self.name), 'w') as f:
            for im in self.__get_import__(out_type):
                f.write('import "{}";\n'.format(im))
            f.write('\n')

            if table_package != '':
                f.write('package {};\n'.format(table_package))
            f.write('\n')
            
            f.write('message {}\n'.format(self.name))
            f.write('{\n')

            for col in self.columns:
                if out_type == col.use_type or col.use_type == TableColumn.COLUMN_TYPE_ALL:
                    if config.judge_user_type(col.type2) != 1:
                        f.write('\t{} {} {} = {}; //{}\n'.format(col.type1, col.type2, col.name, col.idx, col.des))
                    else:
                        user_type = config.get_user_type(col.type2)
                        if user_type.default_value != '': #只有枚举要默认值
                            f.write('\t{} {} {} = {} [default = {}]; //{}\n'.format(col.type1, col.type2, col.name, col.idx, user_type.default_value, col.des))
                        else:
                            f.write('\t{} {} {} = {}; //{}\n'.format(col.type1, col.type2, col.name, col.idx, col.des))

            f.write('}\n\n')

            f.write('message {}_ARRAY\n'.format(self.name))
            f.write('{\n')
            f.write('\trepeated {} rows = 1;\n'.format(self.name))
            f.write('}\n')
