#!/usr/bin/python
# encoding=utf-8

import sys, os

if __name__ == '__main__':
    os.system('protogen.exe -i:' + 'c_table_test.proto' + ' -o:' + 'c_table_test.cs' + ' -p:detectMissing')

