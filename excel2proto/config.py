#!/usr/bin/python
# encoding=utf-8

import xlrd

class UserType(object):
    def __init__(self, name, define_file, default_value):
        self.name = name
        self.define_file = define_file
        self.default_value = default_value

class Config(object):
    def __init__(self):
        self.user_types = []
        data = xlrd.open_workbook('UserDefineType.xlsx')
        table = data.sheets()[0]
        for i in range(table.nrows):
            if i == 0:
                continue
            user_type = UserType(table.cell(i,0).value, table.cell(i,1).value, table.cell(i,2).value)
            self.user_types.append(user_type)

        #用来辅助判非法类型
        self.normal_type = ['sint32', 'uint32', 'string', 'float']

        self.table_path = '../table/'
        self.proto_path = '../proto/'

    def get_user_type(self, name):
        for ut in self.user_types:
            if ut.name == name:
                return ut

    def judge_user_type(self, name):
        for ut in self.user_types:
            if ut.name == name:
                return 1
        if self.normal_type.count(name) <= 0:
            return -1
        return 0
