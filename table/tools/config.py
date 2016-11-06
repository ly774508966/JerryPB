#!/usr/bin/python
# encoding=utf-8

import os

class Config(object):
    def __init__(self):
        self.user_type_table_path = 'UserDefineType.xlsx'
        self.table_path = '../table'
        self.proto_path = '../proto'
        self.client_table_prefix = 'c_table_'
        self.server_table_prefix = 's_table_'
        self.client_table_package = 'Table'
        self.server_table_package = 'table'
        self.table_cs_path = '../output/table_cs' # 表格CS文件存储路径
        self.table_data_path = '../output/table_data' # 表格CS文件存储路径

    @classmethod
    def proto_to_cs(cls, proto_name, cs_path):
        os.system('protogen.exe -i:' + proto_name + ' -o:' + cs_path + ' -p:detectMissing')

    @classmethod
    def generate_proto_py_file(cls, pattern):
        os.system('protoc.exe -I. --python_out=. {}.proto'.format(pattern))
        
        
