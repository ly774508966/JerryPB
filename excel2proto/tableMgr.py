#!/usr/bin/python
# encoding=utf-8

from logger import Logger
from config import Config, UserType

logger = Logger(Logger.LOG_LEVEL_INFO)
config = Config()

class TableColumn(object):
    
    COLUMN_TYPE_NONE   = 0
    COLUMN_TYPE_CLIENT = 1
    COLUMN_TYPE_SERVER = 2
    COLUMN_TYPE_ALL    = 3
    
    def __init__(self):
        self.type1 = ''
        self.type2 = ''
        self.name = ''
        self.idx = 1
        self.des = ''
        self.use_type = self.COLUMN_TYPE_NONE

class TableMgr(object):
    def __init__(self, name, use_type):
        self.use_type = self.__get_use_type__(use_type)
        self.name = name
        self.columns = []
        
    def __get_use_type__(self, data):
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
            if col.use_type != out_type:
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
        if col_type.find('List.') != -1:
            column.type1 = 'repeated'
            column.type2 = col_type.split('.')[1]
        else:
            column.type1 = 'optional'
            column.type2 = col_type
        return column

    def add_column(self, col_type, col_name, col_des, col_use_type, col_idx):
        use_type = self.__get_use_type__(col_use_type)
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

        if self.use_type == TableColumn.COLUMN_TYPE_NONE:
            return

        outFlag = ''
        package_name = ''
        if out_type == TableColumn.COLUMN_TYPE_CLIENT:
            outFlag = 'c_table_'
            package_name = 'Table'
        elif out_type == TableColumn.COLUMN_TYPE_SERVER:
            outFlag = 's_table_'
            package_name = 'table'
        else:
            return
        
        with open('{}{}.proto'.format(outFlag, self.name), 'w') as f:
            for im in self.__get_import__(out_type):
                f.write('import "{}";\n'.format(im))
            f.write('\n')

            if package_name != '':
                f.write('package {};\n'.format(package_name))
            f.write('\n')
            
            f.write('message {}\n'.format(self.name))
            f.write('{\n')

            for col in self.columns:
                if out_type == col.use_type or col.use_type == TableColumn.COLUMN_TYPE_ALL:
                    if config.judge_user_type(col.type2) != 1:
                        f.write('\t{} {} {} = {}; //{}\n'.format(col.type1, col.type2, col.name, col.idx, col.des))
                    else:
                        user_type = config.get_user_type(col.type2)
                        f.write('\t{} {} {} = {} [default = {}]; //{}\n'.format(col.type1, col.type2, col.name, col.idx, user_type.default_value, col.des))

            f.write('}\n\n')

            f.write('message {}_ARRAY\n'.format(self.name))
            f.write('{\n')
            f.write('\trepeated {} rows = 1;\n'.format(self.name))
            f.write('}\n')
