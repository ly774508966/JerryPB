#!/usr/bin/python
# encoding=utf-8

import os

class Config(object):
    def __init__(self):
        self.user_type_table_path = 'UserDefineType.xlsx'
        self.table_path = '../table/'
        self.proto_path = '../proto/'
        self.client_table_prefix = 'c_table_'
        self.server_table_prefix = 's_table_'
        self.client_table_package = 'Table'
        self.server_table_package = 'table'
        self.table_cs_path = '../output/table_cs/' # 表格CS文件存储路径

    @classmethod
    def proto_to_cs(cls, proto_path, proto_name, cs_path):
        work_path = os.getcwd()
        os.chdir(proto_path)
        os.system('protogen.exe -i:' + proto_name + ' -o:' + cs_path + ' -p:detectMissing')
        os.chdir(work_path)

    @classmethod
    def generate_proto_py_file(cls, pattern, path):
        work_path = os.getcwd()
        os.chdir(path)
        os.system('protoc.exe -I. --python_out=. {}.proto'.format(pattern))
        os.chdir(work_path)
        
        
