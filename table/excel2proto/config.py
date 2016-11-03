#!/usr/bin/python
# encoding=utf-8

class Config(object):
    def __init__(self):

        self.user_type_table_path = 'UserDefineType.xlsx'
        self.table_path = '../table/'
        self.proto_path = '../proto/'
        self.client_table_prefix = 'c_table_'
        self.server_table_prefix = 's_table_'
        self.client_table_package = 'Table'
        self.server_table_package = 'table'
