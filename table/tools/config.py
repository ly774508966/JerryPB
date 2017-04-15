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
        self.common_prefix = 'common_'
        self.command_prefix = 'command_'

        self.client_table_package = 'Table'
        self.server_table_package = 'table'
        
        self.table_cs_path = '../output/table_cs' # 表格CS文件存储相对路径
        self.table_data_path = '../output/table_data' # 表格二进制文件存储相对路径
        self.common_cs_path = '../output/common_cs' # 公共PB的CS文件存储相对路径
        self.command_cs_path = '../output/command_cs' # 协议PB的CS文件存储相对路径
        
        self.unity_table_cs_path = '../../Assets/Scripts/Table/proto_gen' # Unity中表格CS文件存储相对路径
        self.unity_table_data_path = '../../Assets/Resources/Table' # Unity中表格二进制文件存储相对路径
        self.unity_common_cs_path = '../../Assets/Scripts/MSG/proto_gen' # Unity中公共PB的CS文件存储相对路径
        self.unity_command_cs_path = '../../Assets/Scripts/MSG/cmd' # Unity中协议PB的CS文件存储相对路径

    @classmethod
    def proto_to_cs(cls, proto_name, cs_path):
        os.system('protogen.exe -i:' + proto_name + ' -o:' + cs_path + ' -p:detectMissing')

    @classmethod
    def generate_proto_py_file(cls, pattern):
        os.system('protoc.exe -I. --python_out=. {}.proto'.format(pattern))

    @classmethod
    def delete_xml(cls, cs_path):
        text = ''
        pattern = '[global::System.Xml.Serialization.XmlIgnore]'
        target = '//Here has been deleted XmlIgnore'
        with open(cs_path, 'r') as f:
            text = f.read()
        if text.count(pattern) > 0:
            with open(cs_path,'w') as f:
                text = text.replace(pattern, target)
                f.write(text)
